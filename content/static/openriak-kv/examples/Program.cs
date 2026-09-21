using System.Net.Http;
using System.Text;
using System.Text.Json;

using var client = new HttpClient { Timeout = TimeSpan.FromSeconds(30) };
var root = Environment.GetEnvironmentVariable("RIAK_HTTP") ?? "http://127.0.0.1:18098";
var url = root + "/buckets/client-demo/keys/aiko";
async Task<(string? Context, string Body)> Request(string method, string address, object? value = null, string? context = null)
{
    using var request = new HttpRequestMessage(new HttpMethod(method), address);
    request.Headers.Add("X-Riak-Index-city_bin", "Tokyo");
    if (context != null) request.Headers.Add("X-Riak-Vclock", context);
    if (value != null) request.Content = new StringContent(JsonSerializer.Serialize(value), Encoding.UTF8, "application/json");
    using var response = await client.SendAsync(request);
    response.EnsureSuccessStatusCode();
    return (response.Headers.TryGetValues("X-Riak-Vclock", out var values) ? values.First() : null,
        await response.Content.ReadAsStringAsync());
}
await Request("PUT", url, new { name = "Aiko", city = "Tokyo" });
var item = await Request("GET", url); Console.WriteLine(item.Body);
await Request("PUT", url, new { name = "Aiko Ng", city = "Tokyo" }, item.Context);
Console.WriteLine((await Request("GET", root + "/buckets/client-demo/index/city_bin/Tokyo")).Body);
item = await Request("GET", url);
using var document = JsonDocument.Parse(item.Body);
if (document.RootElement.GetProperty("name").GetString() != "Aiko Ng") throw new Exception("Update did not match");
await Request("DELETE", url, context: item.Context);
Console.WriteLine("Updated, indexed, and deleted aiko");
