"""APK installation shared by Alpine releases."""
def install(tool, target, context):
    package_path = context["package_path"]
    return f"""# Update installed OS packages from this release's configured repositories.
apk upgrade --no-cache
apk add --no-cache bash ca-certificates coreutils su-exec shadow tzdata
apk add --no-cache --allow-untrusted {package_path}
rm -f {package_path}"""
