#!/usr/bin/env escript
-mode(compile).

%% Runs in an isolated VM, not on a customer's Riak node. Command callbacks
%% are inspected, never invoked. Only registration and usage functions run.
main([Root | ExtraModules]) ->
    code:add_paths(filelib:wildcard(Root ++ "/lib/*/ebin")),
    {ok, _} = application:ensure_all_started(clique),
    ok = clique_config:load_schema([Root ++ "/share/schema"]),
    Beams = filelib:wildcard(Root ++ "/lib/*/ebin/*.beam"),
    Modules = [list_to_atom(filename:basename(P, ".beam")) || P <- Beams],
    Registrars = lists:sort([M || M <- Modules,
        begin code:ensure_loaded(M), erlang:function_exported(M, register_cli, 0) end]),
    Registration = [register(M) || M <- Registrars],
    Registered = lists:sort(ets:tab2list(clique_commands)),
    Builtins = [begin {Spec, _} = clique_command:match(["riak-admin", C]), Spec end
                || C <- ["set", "show", "describe"]],
    Commands = [command(S) || S <- Registered ++ Builtins],
    Usage = [obj([{path, strings(P)}, {help, usage(P)}])
             || {P, _} <- lists:sort(ets:tab2list(clique_usage))],
    ScriptModules = lists:usort(lists:append([script_modules(P) || P <- filelib:wildcard(Root ++ "/bin/riak*")])),
    Relevant = lists:usort(ScriptModules ++ Registrars ++
        [proplists:get_value(module, erlang:fun_info(F)) || {_, _, _, F} <- Registered] ++
        [riak, riak_client, riak_kv_console, riak_core_console, riak_repl_console,
         riak_kv_clusteraae_fsm, clique_parser, clique_config, cuttlefish_escript] ++
         [list_to_atom(M) || M <- ExtraModules]),
    Data = obj([{root, text(Root)}, {registrations, Registration}, {commands, Commands}, {usage, Usage},
                {cuttlefish_options, literal_options(cuttlefish_escript)},
                {modules, [describe_module(M) || M <- Relevant]},
                {available_modules, Modules},
                {apk_database, read_text("/lib/apk/db/installed")},
                {dpkg_database, read_text("/var/lib/dpkg/status")},
                {os_release, read_text("/etc/os-release")},
                {otp_release, text(erlang:system_info(otp_release))}]),
    io:format("OPENRIAK_CLI_JSON_BEGIN~n~s~nOPENRIAK_CLI_JSON_END~n", [mochijson2:encode(Data)]).

script_modules(Path) ->
    case file:read_file(Path) of
        {ok, Data} ->
            case re:run(Data, "\\brpc(?:_raw)?\\s+([a-z][a-zA-Z0-9_]*)\\s+", [global, {capture, [1], list}]) of
                {match, Matches} -> [list_to_atom(M) || [M] <- Matches];
                nomatch -> []
            end;
        _ -> []
    end.

%% Decode a literal getopt declaration, without executing even its producer.
literal_options(Module) ->
    try
        {ok, {_, [{abstract_code, {raw_abstract_v1, Forms}}]}} = beam_lib:chunks(code:which(Module), [abstract_code]),
        [{function,_,cli_options,0,[{clause,_,[],[],[Expression]}]}] =
            [F || F = {function,_,cli_options,0,_} <- Forms],
        [obj([{key, K}, {short, text([S])}, {name, text(L)}, {datatype, term(T)}, {description, text(H)}])
            || {K,S,L,T,H} <- erl_parse:normalise(Expression)]
    catch _:_ -> [] end.

register(M) ->
    try M:register_cli() of
        _ -> obj([{module, M}, {status, ok}])
    catch C:E -> obj([{module, M}, {status, error}, {error, term({C,E})}]) end.

command({Path, Keys, Flags, Callback}) ->
    obj([{path, strings(Path)}, {arguments, specs(Keys)}, {options, specs(Flags)},
         {help, usage(Path)}, {callback, callback(Callback)}]).

specs('_') -> unrestricted;
specs(Specs) -> [spec(S) || S <- Specs].

spec({clique_spec, Key, Name, Short, Datatype, Validator, Typecast}) ->
    obj([{key, Key}, {name, text(Name)},
         {short, case Short of undefined -> null; N when is_integer(N) -> text([N]); _ -> text(Short) end},
         {datatype, term(Datatype)}, {validator, callback(Validator)}, {typecast, callback(Typecast)}]);
spec(Other) -> obj([{unsupported_spec, term(Other)}]).

callback(F) when is_function(F) ->
    Info = erlang:fun_info(F),
    obj([{module, proplists:get_value(module, Info)},
         {function, proplists:get_value(name, Info)}, {arity, proplists:get_value(arity, Info)}]);
callback(_) -> null.

usage([Script, Command]) when Command == "set"; Command == "show"; Command == "describe" ->
    %% These builtins have no ETS usage entry.
    Error = list_to_atom(Command ++ "_no_args"),
    try
        Status = clique_error:format(Script, {error, Error}),
        {Stdout, Stderr} = clique_writer:write(Status, "human"),
        text([Stdout, Stderr])
    catch _:_ -> <<>> end;
usage(Path) ->
    try clique_usage:find(Path) of
        {error, _} -> <<>>;
        Value -> text(Value)
    catch _:_ -> <<>> end.

describe_module(M) ->
    case code:which(M) of
        Path when is_list(Path) ->
            {ok, Bytes} = file:read_file(Path),
            Exports = [obj([{name, N}, {arity, A}]) || {N,A} <- M:module_info(exports)],
            {Source, Functions, Types, Queries} = case beam_lib:chunks(Path, [abstract_code]) of
                {ok, {_, [{abstract_code, {raw_abstract_v1, Forms}}]}} ->
                    {text([erl_pp:form(F) || F <- Forms]),
                     [function_info(F, Forms) || F = {function,_,_,_,_} <- Forms],
                     [text(erl_pp:form(F)) || F = {attribute,_,T,_} <- Forms,
                                             T == type orelse T == opaque],
                     query_forms(Forms)};
                _ -> {null, [], [], []}
            end,
            obj([{module, M}, {sha256, hex(crypto:hash(sha256, Bytes))},
                 {exports, Exports}, {source, Source}, {functions, Functions}, {types, Types}, {query_forms, Queries}]);
        _ -> obj([{module, M}, {missing, true}])
    end.

function_info({function, Line, Name, Arity, Clauses} = F, Forms) ->
    Specs = [text(erl_pp:form(S)) || S = {attribute,_,spec,{{N,A},_}} <- Forms,
                                    N == Name, A == Arity],
    Heads = [text([atom_to_list(Name), "(",
                    lists:join(", ", [erl_pp:expr(A) || A <- Args]), ")"])
             || {clause,_,Args,_,_} <- Clauses],
    obj([{name, Name}, {arity, Arity}, {line, erl_anno:line(Line)},
         {heads, Heads}, {specs, Specs}, {source, text(erl_pp:form(F))}]).

query_forms(Forms) ->
    Types = maps:from_list([{N,T} || {attribute,_,type,{N,T,_}} <- Forms]),
    query_types(maps:get(query_definition, Types, none), Types, []).
query_types({type,_,union,Ts}, Types, Seen) ->
    lists:append([query_types(T, Types, Seen) || T <- Ts]);
query_types({user_type,_,N,_}, Types, Seen) ->
    case lists:member(N, Seen) of true -> []; false -> query_types(maps:get(N, Types, none), Types, [N|Seen]) end;
query_types({type,_,tuple,[{atom,_,Selector}|_]} = T, _, _) ->
    [obj([{selector, Selector}, {signature, text(erl_pp:form({attribute,0,type,{query,T,[]}}))}])];
query_types(_, _, _) -> [].

obj(Fields) -> {struct, Fields}.
strings(Items) -> [text(I) || I <- Items].
text(A) when is_atom(A) -> atom_to_binary(A, utf8);
text(S) -> unicode:characters_to_binary(S).
term(T) -> text(io_lib:format("~tp", [T])).
hex(Bytes) -> text([io_lib:format("~2.16.0b", [B]) || <<B>> <= Bytes]).
read_text(Path) -> case file:read_file(Path) of {ok, Data} -> Data; _ -> null end.
