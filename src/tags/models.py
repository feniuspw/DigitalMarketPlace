from django.db import models
from products.models import Product
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify


# Create your models here.

# NOTA: QUANDO EH MANY TO MANY FIELD VC PODE REFERENCIAR COMO: ex: object.products.all (tag object)
# E SE FOR FOREIGN KEY VC USA object.product_set.all
class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    products = models.ManyToManyField(Product, blank=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)

    @python_2_unicode_compatible
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        view_name = "tags:detail"
        return reverse(view_name, kwargs={"slug": self.slug})


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.slug)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
