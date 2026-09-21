<?php
$base = getenv('RIAK_HTTP') ?: 'http://127.0.0.1:18098';
$url = $base . '/buckets/client-demo/keys/aiko';
function request($method, $url, $value = null, $context = null) {
    $headers = ['Content-Type: application/json', 'X-Riak-Index-city_bin: Tokyo'];
    if ($context !== null) $headers[] = 'X-Riak-Vclock: ' . $context;
    $options = ['method'=>$method, 'header'=>implode("\r\n", $headers), 'timeout'=>30];
    if ($value !== null) $options['content'] = json_encode($value, JSON_THROW_ON_ERROR);
    $body = file_get_contents($url, false, stream_context_create(['http'=>$options]));
    if ($body === false) throw new RuntimeException('HTTP request failed');
    $vclock = null;
    foreach ($http_response_header as $header) {
        if (stripos($header, 'X-Riak-Vclock:') === 0) $vclock = trim(substr($header, 13));
    }
    return [$vclock, $body];
}
request('PUT', $url, ['name'=>'Aiko', 'city'=>'Tokyo']);
[$context, $body] = request('GET', $url); echo $body, "\n";
request('PUT', $url, ['name'=>'Aiko Ng', 'city'=>'Tokyo'], $context);
echo request('GET', $base . '/buckets/client-demo/index/city_bin/Tokyo')[1], "\n";
[$context, $body] = request('GET', $url);
if (json_decode($body, true, 512, JSON_THROW_ON_ERROR)['name'] !== 'Aiko Ng') throw new RuntimeException('Update did not match');
request('DELETE', $url, null, $context);
echo "Updated, indexed, and deleted aiko\n";
