use reqwest::blocking::Client;
use serde_json::{json, Value};
use std::{env, error::Error, time::Duration};

fn request(client: &Client, method: &str, url: &str, value: Option<Value>, context: Option<&str>) -> Result<(Option<String>, String), Box<dyn Error>> {
    let mut req = client.request(method.parse()?, url).header("X-Riak-Index-city_bin", "Tokyo");
    if let Some(v) = value { req = req.json(&v); }
    if let Some(v) = context { req = req.header("X-Riak-Vclock", v); }
    let res = req.send()?.error_for_status()?;
    let context = res.headers().get("X-Riak-Vclock").map(|v| v.to_str().map(str::to_owned)).transpose()?;
    Ok((context, res.text()?))
}
fn main() -> Result<(), Box<dyn Error>> {
    let client = Client::builder().timeout(Duration::from_secs(30)).build()?;
    let base = env::var("RIAK_HTTP").unwrap_or_else(|_| "http://127.0.0.1:18098".into());
    let url = format!("{base}/buckets/client-demo/keys/aiko");
    request(&client, "PUT", &url, Some(json!({"name":"Aiko","city":"Tokyo"})), None)?;
    let (context, body) = request(&client, "GET", &url, None, None)?; println!("{body}");
    request(&client, "PUT", &url, Some(json!({"name":"Aiko Ng","city":"Tokyo"})), context.as_deref())?;
    println!("{}", request(&client, "GET", &format!("{base}/buckets/client-demo/index/city_bin/Tokyo"), None, None)?.1);
    let (context, body) = request(&client, "GET", &url, None, None)?;
    assert_eq!(serde_json::from_str::<Value>(&body)?["name"], "Aiko Ng");
    request(&client, "DELETE", &url, None, context.as_deref())?;
    println!("Updated, indexed, and deleted aiko");
    Ok(())
}
