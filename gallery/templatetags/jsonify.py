import json

from django import template

register = template.Library()

# jsonify 필터
@register.filter(name='jsonify')
def jsonify(value):
    return json.loads(value)