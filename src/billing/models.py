from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

from products.models import Product


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # se quiser, estudar sobre generic foreign keys (deixa escolher qualquer model + id pra associar.)
    # e nao uma em especifico como abaixo
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    success = models.BooleanField(default=True)
    # transaction_id_payment_system = Braintree / Stripe / PayPal / PagSeguro ...
    # payment_method
    # last_four

    @python_2_unicode_compatible
    def __str__(self):
        return str(self.id)
