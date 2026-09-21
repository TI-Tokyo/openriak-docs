import json
import os
from urllib.request import Request, urlopen

base = os.environ.get("RIAK_HTTP", "http://127.0.0.1:18098")
url = base + "/buckets/client-demo/keys/aiko"

def request(method, url, value=None, context=None):
    headers = {"Content-Type": "application/json", "X-Riak-Index-city_bin": "Tokyo"}
    if context:
        headers["X-Riak-Vclock"] = context
    data = None if value is None else json.dumps(value).encode()
    with urlopen(Request(url, data, headers, method=method), timeout=30) as response:
        return response.headers.get("X-Riak-Vclock"), response.read()

request("PUT", url, {"name": "Aiko", "city": "Tokyo"})
context, body = request("GET", url)
print(body.decode())
request("PUT", url, {"name": "Aiko Ng", "city": "Tokyo"}, context)
print(request("GET", base + "/buckets/client-demo/index/city_bin/Tokyo")[1].decode())
context, body = request("GET", url)
assert json.loads(body)["name"] == "Aiko Ng"
request("DELETE", url, context=context)
print("Updated, indexed, and deleted aiko")
