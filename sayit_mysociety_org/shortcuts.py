from django import shortcuts
from django.template import RequestContext


def render(request, template_name, context=None):
    if context is None:
        context = {}
    return shortcuts.render(
        request, template_name, context,
    )
