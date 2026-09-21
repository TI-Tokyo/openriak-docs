const base = process.env.RIAK_HTTP ?? "http://127.0.0.1:18098";
const url = `${base}/buckets/client-demo/keys/aiko`;
async function request(method, url, value, context) {
  const headers = {"Content-Type": "application/json", "X-Riak-Index-city_bin": "Tokyo"};
  if (context) headers["X-Riak-Vclock"] = context;
  const response = await fetch(url, {
    method, headers, body: value === undefined ? undefined : JSON.stringify(value),
    signal: AbortSignal.timeout(30000)
  });
  if (!response.ok) throw new Error(`${response.status}: ${await response.text()}`);
  return {context: response.headers.get("X-Riak-Vclock"), body: await response.text()};
}
await request("PUT", url, {name: "Aiko", city: "Tokyo"});
let object = await request("GET", url);
console.log(object.body);
await request("PUT", url, {name: "Aiko Ng", city: "Tokyo"}, object.context);
console.log((await request("GET", `${base}/buckets/client-demo/index/city_bin/Tokyo`)).body);
object = await request("GET", url);
if (JSON.parse(object.body).name !== "Aiko Ng") throw new Error("Update did not match");
await request("DELETE", url, undefined, object.context);
console.log("Updated, indexed, and deleted aiko");
