from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.


# simples. Se for approved, pode vender
class SellerAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_seller", blank=True)
    active = models.BooleanField(default=False)
    # auto_now_add = salva a hora no momento q foi criado
    # auto_now = salva a hora toda vez que atualizar esta entrada no banco
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    @python_2_unicode_compatible
    def __str__(self):
        return str(self.user.name)
