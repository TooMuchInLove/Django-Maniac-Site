from django import template

register = template.Library()


@register.filter(name='filter_a')
def filter_a(value, arg):
    if value[0] == arg:
        return '+'