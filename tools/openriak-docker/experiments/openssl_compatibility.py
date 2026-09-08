#!/usr/bin/env python3
"""Verify packaged OTP crypto and TLS against an upgraded OpenSSL library."""
import argparse
import json
from pathlib import Path
import sys
import uuid
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import openriak_docker as tool

ERLANG = r'''
{ok, _} = application:ensure_all_started(ssl),
Info = crypto:info(),
io:format("Crypto linkage: ~p~n", [Info]),
dynamic = maps:get(link_type, Info),
true = lists:prefix("OpenSSL " ++ os:getenv("EXPECTED_OPENSSL") ++ " ",
                    maps:get(cryptolib_version_linked, Info)),
<<16#ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad:256>>
    = crypto:hash(sha256, <<"abc">>),
<<16#f7bc83f430538424b13298e6aa6fb143ef4d59a14946175997479dbc2d1a3cd8:256>>
    = crypto:mac(hmac, sha256, <<"key">>, <<"The quick brown fox jumps over the lazy dog">>),
<<16#120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b:256>>
    = crypto:pbkdf2_hmac(sha256, <<"password">>, <<"salt">>, 1, 32),
32 = byte_size(crypto:strong_rand_bytes(32)),
lists:foreach(fun(Cipher) ->
    Key = crypto:strong_rand_bytes(32),
    lists:foreach(fun(Plain) ->
        IV = crypto:strong_rand_bytes(12),
        AAD = <<"OpenRiak OpenSSL compatibility">>,
        {Encrypted, Tag} = crypto:crypto_one_time_aead(Cipher, Key, IV, Plain, AAD, 16, true),
        Plain = crypto:crypto_one_time_aead(Cipher, Key, IV, Encrypted, AAD, Tag, false),
        <<First, Rest/binary>> = Tag,
        error = crypto:crypto_one_time_aead(Cipher, Key, IV, Encrypted, AAD,
                                          <<(First bxor 1), Rest/binary>>, false)
    end, [<<>>, <<"authenticated payload">>])
end, [aes_256_gcm, chacha20_poly1305]),
{PubA, PrivA} = crypto:generate_key(ecdh, prime256v1),
{PubB, PrivB} = crypto:generate_key(ecdh, prime256v1),
Shared = crypto:compute_key(ecdh, PubB, PrivA, prime256v1),
Shared = crypto:compute_key(ecdh, PubA, PrivB, prime256v1),
{ok, PEM} = file:read_file("/tmp/openriak-openssl-test/key.pem"),
[Entry] = public_key:pem_decode(PEM),
Private = public_key:pem_entry_decode(Entry),
Signature = public_key:sign(<<"signed payload">>, sha256, Private),
true = public_key:verify(<<"signed payload">>, sha256, Signature, Private),
false = public_key:verify(<<"tampered payload">>, sha256, Signature, Private),
io:format("PASS hashes, HMAC, PBKDF2, random, AEAD, ECDH and RSA~n"),
lists:foreach(fun({Version, Family, Address}) ->
    Cert = "/tmp/openriak-openssl-test/cert.pem",
    KeyFile = "/tmp/openriak-openssl-test/key.pem",
    {ok, Listener} = ssl:listen(0, [Family, binary, {active,false}, {ip,Address},
                                  {versions,[Version]}, {certfile,Cert}, {keyfile,KeyFile}]),
    {ok, {_, Port}} = ssl:sockname(Listener),
    Parent = self(),
    {Pid, Ref} = spawn_monitor(fun() ->
        {ok, Transport} = ssl:transport_accept(Listener, 10000),
        {ok, Server} = ssl:handshake(Transport, 10000),
        {ok, <<"request">>} = ssl:recv(Server, 7, 10000),
        ok = ssl:send(Server, <<"response">>),
        ok = ssl:close(Server),
        Parent ! {self(), passed}
    end),
    {ok, Client} = ssl:connect("localhost", Port,
        [Family, binary, {active,false}, {versions,[Version]}, {verify,verify_peer},
         {cacertfile,"/tmp/openriak-openssl-test/ca.pem"}, {server_name_indication,"localhost"},
         {customize_hostname_check,[{match_fun,public_key:pkix_verify_hostname_match_fun(https)}]}], 10000),
    {ok, [{protocol, Version}]} = ssl:connection_information(Client, [protocol]),
    ok = ssl:send(Client, <<"request">>),
    {ok, <<"response">>} = ssl:recv(Client, 8, 10000),
    ok = ssl:close(Client),
    receive
        {Pid, passed} -> ok;
        {'DOWN', Ref, process, Pid, Reason} -> error({tls_server_failed, Reason})
    after 10000 -> error(tls_server_timeout)
    end,
    erlang:demonitor(Ref, [flush]),
    ok = ssl:close(Listener),
    io:format("PASS certificate-verified ~p over ~p~n", [Version, Family])
end, [{V, F, A} || V <- ['tlsv1.2', 'tlsv1.3'],
                    {F, A} <- [{inet, {127,0,0,1}}, {inet6, {0,0,0,0,0,0,0,1}}]]),
halt(0).
'''
SHELL = r'''set -eu
export EXPECTED_OPENSSL="$1"
mkdir -p /tmp/openriak-openssl-test
openssl version -a
dpkg-query -W libssl3 openssl
cd /tmp/openriak-openssl-test
openssl req -x509 -newkey rsa:2048 -nodes -days 1 -sha256 -subj '/CN=OpenRiak test CA' -addext basicConstraints=critical,CA:TRUE -addext keyUsage=critical,keyCertSign,cRLSign -keyout ca.key -out ca.pem
openssl req -new -newkey rsa:2048 -nodes -sha256 -subj /CN=localhost -keyout key.pem -out request.pem
printf 'basicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\nsubjectAltName=DNS:localhost\n' > extensions.cnf
openssl x509 -req -in request.pem -CA ca.pem -CAkey ca.key -CAcreateserial -days 1 -sha256 -extfile extensions.cnf -out cert.pem
for bundled_erl in /usr/lib/riak/erts-*/bin/erl
do
    runtime_root=${bundled_erl%/erts-*}
    for crypto_nif in "$runtime_root"/lib/crypto-*/priv/lib/crypto.so
    do
        ldd "$crypto_nif"
        sha256sum "$crypto_nif"
    done
    sha256sum "$runtime_root"/erts-*/bin/beam.smp
    exec "$bundled_erl" +S 2:2 +SDcpu 1 +SDio 1 +A 1 -boot "$runtime_root/bin/no_dot_erlang" -pa "$runtime_root"/lib/*/ebin -noshell -eval "$2"
done
exit 1
'''


def verify(image, output, version='3.0.22', timeout=1800):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    name = 'openriak-openssl-check-' + uuid.uuid4().hex[:12]
    state = {'image': image, 'expected_openssl': version, 'started_at': tool.isoformat()}
    try:
        tool.run_logged([tool.docker_command(), 'run', '--rm', '--name', name,
            '--platform', 'linux/amd64', '--network', 'none', '--entrypoint', 'sh',
            image, '-ec', SHELL, 'openssl-check', version, ERLANG],
            output / 'openssl-compatibility.log', timeout_seconds=timeout)
        state['status'] = 'passed'
    except Exception as error:
        state.update(status='failed', error=str(error))
        raise
    finally:
        tool.run_logged([tool.docker_command(), 'rm', '-f', name],
                        output / 'openssl-compatibility-cleanup.log', check=False, timeout_seconds=timeout)
        state['finished_at'] = tool.isoformat()
        (output / 'openssl-compatibility.json').write_text(json.dumps(state, indent=2) + '\n')
    return state


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--version', default='3.0.22')
    parser.add_argument('--timeout', type=int, default=1800)
    args = parser.parse_args()
    print(json.dumps(verify(args.image, args.output, args.version, args.timeout), indent=2))
