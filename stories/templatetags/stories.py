from django import template
from django.utils.html import mark_safe
from markdown import markdown as md

register = template.Library()


@register.filter
def clip(value, chars):
    if chars > 0 and len(value) > chars:
        value = "%s..." % value[:chars]
    return value


@register.filter
def markdown(value):
    return mark_safe(md(value))
