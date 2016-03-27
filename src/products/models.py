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

# ------------------- THUMBNAIL GENERATION LIBRARIES -------------------
import os
import random
import shutil
from PIL import Image

from django.core.files import File
# ----------------------------------------------------------------------


# handles the upload process
def download_media_location(instance, filename):
    return "%s/%s" % (instance.slug, filename)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # n to n database relationship
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
    media = models.ImageField(blank=True,
                             null=True,
                             upload_to=download_media_location,
                             storage=FileSystemStorage(location=settings.PROTECTED_ROOT)
                             )
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, unique=True, max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=100,decimal_places=2,default=9.99)
    sale_active = models.BooleanField(default=False)
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

    # @property transforma esse metodo em uma property da classe, um atributo. ou seja, nao precisa mais
    # chamar como product_object.get_price(). Agora pode-se chamar como product_object.get_price
    # como se fosse um product_object.slug ou .title
    @property
    def get_price(self):
        if self.sale_price and self.sale_active:
            return self.sale_price
        return self.price

    """
    get thumbnails -> instance.thumbnail_set.all() => because thumbnail has a foreign key to Product
    """


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


# # tentando atualizar tabela myProducts automaticamente
# def product_update_myproducts_post_save_receiver(sender, instance, *args, **kwargs):
#     # cada usuario eh unico. por isso que eu chamo o metodo abaixo com [0] no final.. ja que vai retornar
#     # uma query so.
#     # todo: verificar se nao e necessario fazer verificacao se caso a query nao retorne nada
#     # nota ao To do acima. Acho que nao e necessario. pois so cria-se um produto se ja existe um usuario.
#     # todo: talvez criar trigger no banco seja mais rapido... na verdade eh. MUDAR ISSO PRA TRIGGER NO BANCO!!!!
#     myproducts = MyProducts.objects.filter(user=instance.user)[0]
#     myproducts.products.add(instance)
#     myproducts.save()
#
# post_save.connect(product_update_myproducts_post_save_receiver, sender=Product)


def thumbnail_location(instance, filename):
    return "%s/%s" % (instance.product.slug, filename)

THUMB_CHOICES= (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)


class Thumbnail(models.Model):
    product = models.ForeignKey(Product)
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    width = models.CharField(max_length=20, null=True, blank=True)
    heigth = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
            width_field = "width",
            height_field = "heigth",
            blank=True,
            null=True,
            upload_to=thumbnail_location,
            )

    @python_2_unicode_compatible
    def __str__(self):
        return str(self.media.path)


def create_new_thumb(media_path, instance, owner_slug, max_heigth, max_width):
    # path + filename
    filename = os.path.basename(media_path)
    thumb = Image.open(media_path)
    size = (max_heigth, max_width)
    thumb.thumbnail(size, Image.ANTIALIAS)
    temp_loc = "%s/%s/tmp" % (settings.MEDIA_ROOT, owner_slug)
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)
    temp_file_path = os.path.join(temp_loc, filename)
    # atencao! solucao meio porca
    if os.path.exists(temp_file_path):
        temp_path = os.path.join(temp_loc, "%s" % random.random(), filename)
        os.makedirs(temp_path)
        temp_file_path = os.path.join(temp_path, filename)

    temp_image = open(temp_file_path, "w")
    thumb.save(temp_file_path)
    thumb_data = open(temp_file_path, "rb")

    thumb_file = File(thumb_data)
    instance.media.save(filename, thumb_file)
    temp_image.close()
    thumb_data.close()
    shutil.rmtree(temp_loc, ignore_errors=True)
    return


def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        # get or create instance
        hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
        sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
        micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

        hd_max = (400, 400)
        sd_max = (200, 200)
        micro_max = (50, 50)
        media_path = instance.media.path
        owner_slug = instance.slug
        if hd_created:
            create_new_thumb(media_path, hd, owner_slug, hd_max[0], hd_max[1])
        if sd_created:
            create_new_thumb(media_path, sd, owner_slug, sd_max[0], sd_max[1])
        if micro_created:
            create_new_thumb(media_path, micro, owner_slug, micro_max[0], micro_max[1])


post_save.connect(product_post_save_receiver, sender=Product)


class MyProducts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    products = models.ManyToManyField(Product, blank=True)

    @python_2_unicode_compatible
    def __str__(self):
        return "%s : %s product(s)" %(self.user, self.products.count())

    class Meta:
        verbose_name = "My Products"

