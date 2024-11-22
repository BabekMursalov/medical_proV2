from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    """
    Get an attribute dynamically from an object for Django templates.
    """
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None


