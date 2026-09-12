"""RPM installation; OS layers supply repository and dependency differences."""
def install(tool, target, context):
    package_path = context['package_path']
    if not context['official_rpm']:
        return fallback(tool, target, context)
    repository_setup = context['repository_setup']
    dependencies = context['dependencies']
    suse_openssl = context['suse_openssl']
    release_option = context['release_option']
    runtime_cleanup = context['runtime_cleanup']
    return f"""{repository_setup}# Update installed OS packages before installing the OpenRiak KV package.
if command -v dnf >/dev/null 2>&1
then
    dnf upgrade --refresh -y{release_option}
    dnf install -y{release_option} {dependencies}
    dnf clean all
elif command -v microdnf >/dev/null 2>&1
then
    microdnf upgrade --refresh -y
    microdnf install -y dnf
    dnf install -y {dependencies}
    dnf clean all
elif command -v yum >/dev/null 2>&1
then
    yum clean expire-cache
    yum update -y
    yum install -y {dependencies}
    yum clean all
elif command -v zypper >/dev/null 2>&1
then
    zypper --non-interactive refresh
    zypper --non-interactive update --no-recommends
    zypper --non-interactive install --no-recommends bash ca-certificates gawk glibc hostname libgcc_s1 libstdc++6 libncurses6 {suse_openssl} pam procps shadow sudo util-linux libz1 timezone
    zypper clean --all
else
    echo 'No supported RPM package manager found' >&2
    exit 1
fi
# These RPMs bundle their matching OTP runtime, including escript, but their
# generated dependency metadata requires /usr/bin/escript outside the payload.
rpm -Uvh --replacepkgs --nodeps {package_path}
if [ ! -e /usr/bin/escript ]
then
    for bundled_escript in /usr/lib64/riak/erts-*/bin/escript /usr/lib/riak/erts-*/bin/escript
    do
        if [ -x "$bundled_escript" ]
        then
            ln -s "$bundled_escript" /usr/bin/escript
            break
        fi
    done
fi
test -x /usr/bin/escript
# Check the bundled runtime and its OpenSSL NIF before starting integration tests.
for bundled_erl in /usr/lib64/riak/erts-*/bin/erl /usr/lib/riak/erts-*/bin/erl
do
    if [ -x "$bundled_erl" ]
    then
        runtime_root=${{bundled_erl%/erts-*}}
        "$bundled_erl" +S 2:2 -boot "$runtime_root/bin/no_dot_erlang" -pa "$runtime_root"/lib/crypto-*/ebin -noshell -eval 'crypto:strong_rand_bytes(1), halt().'
        break
    fi
done
{runtime_cleanup}# Clear caches from every package manager used in this installation layer.
# In particular, dnf clean all does not clear microdnf's /var/cache/yum.
rm -rf /var/cache/dnf /var/cache/yum /var/cache/zypp
rm -f {package_path}"""


def fallback(tool, target, context):
    package_path = context["package_path"]
    return f"""# Update installed OS packages before installing the OpenRiak KV package.
if command -v dnf >/dev/null 2>&1
then
    dnf upgrade --refresh -y
    dnf install -y ca-certificates procps-ng shadow-utils tzdata {package_path}
    dnf clean all
elif command -v microdnf >/dev/null 2>&1
then
    microdnf upgrade --refresh -y
    microdnf install -y ca-certificates procps-ng shadow-utils tzdata {package_path}
    microdnf clean all
elif command -v yum >/dev/null 2>&1
then
    yum clean expire-cache
    yum update -y
    yum install -y ca-certificates procps-ng shadow-utils tzdata {package_path}
    yum clean all
elif command -v zypper >/dev/null 2>&1
then
    zypper --non-interactive refresh
    zypper --non-interactive update --no-recommends
    zypper --non-interactive install -y ca-certificates procps timezone {package_path}
    zypper clean --all
else
    echo 'No supported RPM package manager found' >&2
    exit 1
fi
# Clear caches from every package manager used in this installation layer.
# In particular, dnf clean all does not clear microdnf's /var/cache/yum.
rm -rf /var/cache/dnf /var/cache/yum /var/cache/zypp
rm -f {package_path}"""
