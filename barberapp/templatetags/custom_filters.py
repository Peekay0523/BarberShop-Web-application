from django import template

register = template.Library()

@register.filter
def contains(value, substring):
    """
    Check if value contains substring (case-insensitive)
    """
    if not value or not substring:
        return False
    return str(substring).lower() in str(value).lower()