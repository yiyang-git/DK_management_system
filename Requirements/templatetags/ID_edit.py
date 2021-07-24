from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def ID_edit(value, ID_str):
    get_str = ID_str + str(value)
    return mark_safe(get_str)


register.filter(ID_edit)
