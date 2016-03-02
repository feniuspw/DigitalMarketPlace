from django.db import models
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify

# Generate unique slugs
from random import shuffle, choice, randint
import string

# put foreign key equal to the default django user model
from django.conf import settings

# Library for get_absolute_url
from django.core.urlresolvers import reverse
# Reverse: Takes an URL name or View name and makes it more dynamic

# ================================================================
# __str__ -> python 3.x
# __unicode__ -> python 2.x
# in order to use __str__ and be compatible import:
from django.utils.encoding import python_2_unicode_compatible
# and use @python_2_unicode_compatible on top of __str__ function.
# ================================================================

# ------------------ FILE PROTECTION ------------------
from django.core.files.storage import FileSystemStorage
# -----------------------------------------------------


# handles the upload process
def download_media_location(instance, filename):
    return "%s/%s" %(instance.id, filename)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # n to n database relationship
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
    media = models.FileField(blank=True,
                             null=True,
                             upload_to=download_media_location,
                             storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
                             )
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True, max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100,decimal_places=2,default=9.99)
    sale_price = models.DecimalField(max_digits=100,decimal_places=2,default=6.99,null=True,blank=True)

    @python_2_unicode_compatible
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        view_name = "products:detail_slug"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_download(self):
        view_name = "products:download_slug"
        url = reverse(view_name, kwargs={"slug": self.slug})
        return url

# make sure that the product does not already exists
def create_slug(instance):
    # LEMBRAR DE TESTAR ESCAPE STRING POR SEGURANCA DO BANCO!!!!
    # VER SE A DESCRICAO COMECAR COM ' OU " NAO VAI DAR PAU NO BANCO E INJETAR CODIGO MALICIOSO

    # TESTAR O WHILE LOOP PRA VER SE NAO VAI DAR PAU NESSA PORRA!!!

    pre_slug = instance.description[:15].split(" ")
    shuffle(pre_slug)
    pre_slug = ' '.join(pre_slug)
    slug = slugify(instance.title[:42]+" " + pre_slug)
    qs = Product.objects.filter(slug=slug).exists()
    if qs:
        pre_slug = instance.description[:15].split(" ")
        shuffle(pre_slug)
        rnd = [choice(string.ascii_letters + string.digits) for n in range(7)]
        shuffle(rnd)
        rnd = ''.join(rnd)
        pre_slug = ' '.join(pre_slug)+" "+rnd
        slug = slugify(instance.title[:30] + " " + pre_slug)
        while True:
            qs = Product.objects.filter(slug=slug).exists()
            if qs:
                slug += "-" + str(randint(0, 2000000))
            else:
                break
    return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)


class MyProducts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product, blank=True)

    @python_2_unicode_compatible
    def __str__(self):
        return "%s" % self.products.count()

    class Meta:
        verbose_name = "My Products"
        verbose_name_plural = "My Products"
