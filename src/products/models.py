from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# ================================================================
# __str__ -> python 3.x
# __unicode__ -> python 2.x
# in order to use __str__ and be compatible import:
from django.utils.encoding import python_2_unicode_compatible
# and use @python_2_unicode_compatible on top of __str__ function.
# ================================================================


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)  # unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=100,decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits=100,decimal_places=2,default=6.99,null=True,blank=True)

    @python_2_unicode_compatible
    def __str__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
        """  if not instance.slug:
                a = instance.title.split(" ")
                string = a[0]
                for i in a[1:]:
                    string += "-"+i
                instance.slug = string"""


pre_save.connect(product_pre_save_receiver, sender=Product)