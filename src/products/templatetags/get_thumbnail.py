from django import template
# in order to check if obj is really a Product and arg is a correct filter argument we must import THUMB_CHOICES and
# Product
from ..models import Product, THUMB_CHOICES

register = template.Library()


@register.filter
def get_thumbnail(obj, arg):
    """
    :param obj: Product
    :param arg: String (filter)
    :return: String. Thumbnail media url
    """
    arg = arg.lower()
    if not isinstance(obj, Product):
        raise TypeError("This is not a valid product model")
    choices = dict(THUMB_CHOICES)
    if not choices.get(arg):
        raise TypeError("This is not a valid type for this model")
    obj = obj.thumbnail_set.filter(type=arg).first()
    if hasattr(obj, 'media'):
        return obj.media.url
    return obj
