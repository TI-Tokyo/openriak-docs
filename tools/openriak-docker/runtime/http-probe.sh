set -eu
export OPENRIAK_HTTP_PROBE_TIMEOUT_MS="$2"
for bundled_erl in /usr/lib64/riak/erts-*/bin/erl /usr/lib/riak/erts-*/bin/erl
do
    if [ -x "$bundled_erl" ]
    then
        runtime_root=${bundled_erl%/erts-*}
        exec "$bundled_erl" +S 1:1 +SDcpu 1 +SDio 1 +A 1 -boot "$runtime_root/bin/no_dot_erlang" -noshell -eval "$1"
    fi
done
echo 'Bundled Erlang runtime not found for HTTP probe' >&2
exit 1
