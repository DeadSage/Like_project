from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_save=True)
def currency(value, name='руб.'):
    return mark_safe('%1.2f %s' % (value, name))


# register.filter('currency', currency)
