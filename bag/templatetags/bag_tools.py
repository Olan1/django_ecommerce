from django import template


# To register filter - Used to create custom template tags and filters
register = template.Library()
# Register function as a template filter
@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity