"""rhel 9 reusable base settings; inherit shared EL9 patch construction."""
from builders_base.enterprise_linux.v9 import common as el9
from builders_base.enterprise_linux.v9.common import render_stage, runtime_check


def configure(target, context):
    el9.configure(target, context)
    context['os_release'] = '9'
