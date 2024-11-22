from django import template

register = template.Library()

@register.filter
def split(value, delimiter=","):
    """String-i delimiter ilə parçalayır."""
    return value.split(delimiter)
