require 'net/http'
require 'json'
base = ENV.fetch('RIAK_HTTP', 'http://127.0.0.1:18098')
url = base + '/buckets/client-demo/keys/aiko'
def request(method, url, value = nil, context = nil)
  uri = URI(url)
  klass = {'PUT'=>Net::HTTP::Put, 'GET'=>Net::HTTP::Get, 'DELETE'=>Net::HTTP::Delete}.fetch(method)
  req = klass.new(uri)
  req['Content-Type'] = 'application/json'
  req['X-Riak-Index-city_bin'] = 'Tokyo'
  req['X-Riak-Vclock'] = context if context
  req.body = JSON.generate(value) unless value.nil?
  res = Net::HTTP.start(uri.host, uri.port, read_timeout: 30) { |http| http.request(req) }
  raise "#{res.code}: #{res.body}" unless res.is_a?(Net::HTTPSuccess)
  [res['X-Riak-Vclock'], res.body]
end
request('PUT', url, {name: 'Aiko', city: 'Tokyo'})
context, body = request('GET', url)
puts body
request('PUT', url, {name: 'Aiko Ng', city: 'Tokyo'}, context)
puts request('GET', base + '/buckets/client-demo/index/city_bin/Tokyo')[1]
context, body = request('GET', url)
raise 'Update did not match' unless JSON.parse(body)['name'] == 'Aiko Ng'
request('DELETE', url, nil, context)
puts 'Updated, indexed, and deleted aiko'
