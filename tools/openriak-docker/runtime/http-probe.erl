
Timeout = list_to_integer(os:getenv("OPENRIAK_HTTP_PROBE_TIMEOUT_MS")),
case gen_tcp:connect({127,0,0,1}, 8098, [binary, {active,false}], Timeout) of
    {ok, Socket} ->
        ok = gen_tcp:send(Socket, <<"GET /ping HTTP/1.0\r\nHost: localhost\r\nConnection: close\r\n\r\n">>),
        Receive = fun Again() ->
            case gen_tcp:recv(Socket, 0, Timeout) of
                {ok, Data} -> ok = file:write(standard_io, Data), Again();
                {error, closed} -> halt(0);
                {error, Reason} -> io:format(standard_error, "HTTP receive failed: ~p~n", [Reason]), halt(1)
            end
        end,
        Receive();
    {error, Reason} ->
        io:format(standard_error, "HTTP connect failed: ~p~n", [Reason]), halt(1)
end.
