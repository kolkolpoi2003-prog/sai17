from django import template

register = template.Library()

@register.filter
def eq(value, arg):
    """
    Compares two values for equality.
    Usage: {% if value|eq:arg %}
    """
    return value == arg

@register.filter
def mul(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ quantity|mul:price }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def split(value, arg):
    """
    Splits the string by the argument.
    """
    return value.split(arg)
