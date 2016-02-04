from django.db import models

# ================================================================
# __str__ -> python 3.x
# __unicode__ -> python 2.x
# in order to use __str__ and be compatible import:
from django.utils.encoding import python_2_unicode_compatible
# and use @python_2_unicode_compatible on top of __str__ function.
# ================================================================


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=100,decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits=100,decimal_places=2,default=6.99,null=True,blank=True)


    @python_2_unicode_compatible
    def __str__(self):
        return self.title