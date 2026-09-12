"""Oracle Linux family installation policy."""
def configure(tool, target, context):
    context["official_rpm"] = True
