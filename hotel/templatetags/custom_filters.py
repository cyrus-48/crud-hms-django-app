# custom_filters.py
from django import template
from urllib.parse import unquote

register = template.Library()

@register.filter(name='urldecode')
def urldecode(value):
    return unquote(value)
