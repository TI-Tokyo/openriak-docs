#!/usr/bin/env escript
main(_) ->
    {ok, _} = application:ensure_all_started(inets),
    Base = os:getenv("RIAK_HTTP", "http://127.0.0.1:18098"),
    URL = Base ++ "/buckets/client-demo/keys/aiko",
    request(put, URL, <<"{\"name\":\"Aiko\",\"city\":\"Tokyo\"}">>, undefined),
    {Context, Body} = request(get, URL, undefined, undefined),
    io:format("~s~n", [Body]),
    request(put, URL, <<"{\"name\":\"Aiko Ng\",\"city\":\"Tokyo\"}">>, Context),
    {_, Matches} = request(get, Base ++ "/buckets/client-demo/index/city_bin/Tokyo", undefined, undefined),
    io:format("~s~n", [Matches]),
    {NewContext, Updated} = request(get, URL, undefined, undefined),
    true = binary:match(Updated, <<"Aiko Ng">>) =/= nomatch,
    request(delete, URL, undefined, NewContext),
    io:format("Updated, indexed, and deleted aiko~n").

request(Method, URL, Body, Context) ->
    H0 = [{"X-Riak-Index-city_bin", "Tokyo"}],
    H = case Context of undefined -> H0; _ -> [{"X-Riak-Vclock", Context}|H0] end,
    Request = case Body of undefined -> {URL, H}; _ -> {URL, H, "application/json", Body} end,
    {ok, {{_, Status, _}, Headers, Result}} = httpc:request(Method, Request, [{timeout, 30000}], [{body_format, binary}]),
    case Status >= 200 andalso Status < 300 of
        true -> {proplists:get_value("x-riak-vclock", Headers), Result};
        false -> error({http_failure, Status, Result})
    end.
