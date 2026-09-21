package main

import (
    "fmt"
    "io"
    "net/http"
    "os"
    "strings"
    "time"
)

var client = &http.Client{Timeout: 30 * time.Second}
func request(method, url, body, context string) (string, string) {
    req, err := http.NewRequest(method, url, strings.NewReader(body)); if err != nil { panic(err) }
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("X-Riak-Index-city_bin", "Tokyo")
    if context != "" { req.Header.Set("X-Riak-Vclock", context) }
    res, err := client.Do(req); if err != nil { panic(err) }; defer res.Body.Close()
    data, err := io.ReadAll(res.Body); if err != nil { panic(err) }
    if res.StatusCode < 200 || res.StatusCode >= 300 { panic(fmt.Sprintf("%d: %s", res.StatusCode, data)) }
    return res.Header.Get("X-Riak-Vclock"), string(data)
}
func main() {
    base := os.Getenv("RIAK_HTTP"); if base == "" { base = "http://127.0.0.1:18098" }
    url := base + "/buckets/client-demo/keys/aiko"
    request("PUT", url, `{"name":"Aiko","city":"Tokyo"}`, "")
    context, body := request("GET", url, "", ""); fmt.Println(body)
    request("PUT", url, `{"name":"Aiko Ng","city":"Tokyo"}`, context)
    _, body = request("GET", base + "/buckets/client-demo/index/city_bin/Tokyo", "", ""); fmt.Println(body)
    context, body = request("GET", url, "", "")
    if !strings.Contains(body, "Aiko Ng") { panic("Update did not match") }
    request("DELETE", url, "", context)
    fmt.Println("Updated, indexed, and deleted aiko")
}
