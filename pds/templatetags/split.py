from django import template

register = template.Library()

# split 필터
@register.filter(name='split')
def split(value, key):
    return value.split(key)