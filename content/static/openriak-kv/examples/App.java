import java.net.URI;
import java.net.http.*;
import java.time.Duration;

class App {
    static final HttpClient client = HttpClient.newHttpClient();
    static HttpResponse<String> request(String method, String url, String body, String context) throws Exception {
        var b = HttpRequest.newBuilder(URI.create(url)).timeout(Duration.ofSeconds(30))
            .header("Content-Type", "application/json").header("X-Riak-Index-city_bin", "Tokyo");
        if (context != null) b.header("X-Riak-Vclock", context);
        b.method(method, body == null ? HttpRequest.BodyPublishers.noBody() : HttpRequest.BodyPublishers.ofString(body));
        var r = client.send(b.build(), HttpResponse.BodyHandlers.ofString());
        if (r.statusCode() < 200 || r.statusCode() >= 300) throw new Exception(r.statusCode() + ": " + r.body());
        return r;
    }
    public static void main(String[] args) throws Exception {
        var base = System.getenv().getOrDefault("RIAK_HTTP", "http://127.0.0.1:18098");
        var url = base + "/buckets/client-demo/keys/aiko";
        request("PUT", url, "{\"name\":\"Aiko\",\"city\":\"Tokyo\"}", null);
        var object = request("GET", url, null, null);
        System.out.println(object.body());
        request("PUT", url, "{\"name\":\"Aiko Ng\",\"city\":\"Tokyo\"}", object.headers().firstValue("X-Riak-Vclock").orElseThrow());
        System.out.println(request("GET", base + "/buckets/client-demo/index/city_bin/Tokyo", null, null).body());
        object = request("GET", url, null, null);
        if (!object.body().contains("Aiko Ng")) throw new Exception("Update did not match");
        request("DELETE", url, null, object.headers().firstValue("X-Riak-Vclock").orElseThrow());
        System.out.println("Updated, indexed, and deleted aiko");
    }
}
