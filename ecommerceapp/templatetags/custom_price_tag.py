from django import template

register = template.Library()

@register.filter
def rupees(price):
    return f'Rs.{price}'