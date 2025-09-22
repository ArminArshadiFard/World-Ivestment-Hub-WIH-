from django import template
from django.conf import settings

# from home.models import Product

register = template.Library()


#
#
# @register.simple_tag
# def mul(x, y):
#     z = float(x) * float(y)
#     z = format(z, ".3f")
#     return z
#
#
@register.simple_tag
def version_css(model_object):
    value = "%s%s?v=%s" % (settings.STATIC_URL, model_object, settings.VERSION_CSS)
    return value


@register.simple_tag
def version_js(model_object):
    value = "%s%s?v=%s" % (settings.STATIC_URL, model_object, settings.VERSION_JS)
    return value
