"""Select the newest repository snapshot within Amazon Linux 2023."""
def configure(tool, target, context):
    context['release_option'] = ' --releasever=latest'
    context['repository_setup'] += '# Use the newest Amazon Linux 2023 repository snapshot during this tested build.\n'
