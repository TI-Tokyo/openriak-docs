import sys,json,pathlib
sys.path.insert(0,'tools/openriak-docker')
import openriak_docker as t
root=pathlib.Path('tools/cache/openriak-docker-minimal-validation/20260908T070450.695815Z/3.4.0/3.4.0-debian-12-otp24')
state=json.loads((root/'validation.json').read_text());base=state['base_images']['linux/amd64']['pinned']
name='openriak-openssl-upstream-check-20260908'
log=pathlib.Path('/tmp/openriak-openssl-upstream-suites.log')
script='''set -eu
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends build-essential debhelper m4 bc dpkg-dev ca-certificates libio-socket-inet6-perl netbase
cd /build/openssl-3.0.22
# Run the unmodified tests, including IPv6, against the preserved build binaries.
make -C build_static test
make -C build_shared test
'''
result={'base':base,'started_at':t.isoformat()}
try:
 t.run_logged([t.docker_command(),'run','--rm','--name',name,'--platform','linux/amd64','--mount','type=bind,src=/tmp/openriak-openssl-full-suite,dst=/build','--entrypoint','sh',base,'-ec',script],log,timeout_seconds=1800)
 result['status']='passed'
finally:
 t.run_logged([t.docker_command(),'rm','-f',name],pathlib.Path('/tmp/openriak-openssl-upstream-cleanup.log'),check=False,timeout_seconds=60)
 result['finished_at']=t.isoformat()
 pathlib.Path('/tmp/openriak-openssl-upstream-suites.json').write_text(json.dumps(result,indent=2)+'\n')
