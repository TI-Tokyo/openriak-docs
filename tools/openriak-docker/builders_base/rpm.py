"""Shared labels and formatting for minimal RPM base images."""
import json


def render_header(target, tool, context):
    identity = target.identity
    mode = tool.minimal.configuration(target)
    tag = mode['base_image']
    source = tool.annotate_artifact('# syntax=docker/dockerfile:1.7\n', 'Dockerfile',
                                    f'{identity.namespace}/{tag}')
    source += '# Reusable minimal OS base; no OpenRiak KV package or Erlang cookie is installed.\n'
    source += '# BuildKit supplies TARGETARCH from --platform.\n\n'
    return source


def render_footer(target, tool, context):
    identity = target.identity
    tag = tool.minimal.configuration(target)['base_image']
    source = ''
    labels = {
        'org.opencontainers.image.title': f'{target.family} {target.release} for OpenRiak',
        'org.opencontainers.image.description': context['description'],
        'org.opencontainers.image.vendor': identity.vendor,
        'org.opencontainers.image.source': identity.source,
        'org.opencontainers.image.url': identity.url,
        'org.opencontainers.image.version': tag.split(':')[1],
        'org.openriak.os.name': target.family,
        'org.openriak.os.release': context['os_release'],
        'org.openriak.os.version': target.release,
        **context['patch_labels'],
    }
    source += '\nFROM package-${TARGETARCH} AS final\n'
    source += '\n'.join(f'LABEL {key}={json.dumps(value)}' for key, value in labels.items())
    return source + '''
# Standard executable search path for the minimal runtime.
ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
CMD ["bash"]
'''
