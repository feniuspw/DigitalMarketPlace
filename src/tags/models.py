from django.db import models
from products.models import Product
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save,post_save
from django.utils.text import slugify


# Create your models here.

# essa eh uma outra maneira de pegar queries.
class TagQuerySet(models.query.QuerySet):

    def active(self):
        return self.filter(active=True)


class TagManager(models.Manager):

    # esse metodo nao eh o mesmo get_queryset da model. ele so chama a classe acima com o metodo q vc quiser definido la
    # pode usar o .all() normalmente. e pode adicionar os metodos acima depois do .all(). por exemplo: .all().active()
    # eh so outra forma de puxar as query_set do banco.
    # def get_queryset(self):             # usando o banco de dados atual
    #     return TagQuerySet(self.model, using=self.db)

    def all(self, *args, **kwargs):
        return super(TagManager, self).all(*args, **kwargs).filter(active=True)

    # da pra fazer dessa forma tb
    # def active(self, *args, **kwargs):
    #     return self.get_queryset().filter(acive=True)
    # dai vc pode chamar no lugar de .all(), .active() mas nao eh uma boa tecnica ja q vc pode esquecer os nomes
    # q vc deu pros metodos da classe. O ideal eh usar o all pq vc ja conhece
    # o modo da classe acima tb deixa fazer a mesma coisa (eh tudo igual de maneiras diferentes haha)
    """
    da pra usar essa classe manager pra criar coisas tb.
    da pra definir um metodo que cria algum objeto ou que seta valores, tanto faz.
    dai vc chama la como Tag.objects(ou o nome q for aqui).meumetodo()
    e retorna o que precisar
    """

"""
Mindblow:
olhe para classe abaixo:
ela eh uma model
quando chamamos Tag.objects.all() por exemplo
chamamos Tag(classe Tag)
         .objects(atributo. se n setado eh default c esse nome)
         .all()(metodo padrao ou nao, como descrito nos comentarios acima. Vc decide)
"""


# NOTA: QUANDO EH MANY TO MANY FIELD VC PODE REFERENCIAR COMO: ex: object.products.all (tag object)
# E SE FOR FOREIGN KEY VC USA object.product_set.all
class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    products = models.ManyToManyField(Product, blank=True)
    slug = models.SlugField(unique=True)
    active = models.BooleanField(default=True)

    # essa variavel chama TagManager pra filtrar resultados sempre que chamarem tag.algumacoisa.all()
    # ou seja.. sempre que chamarem todas as tags do banco, passa por esse filtro
    objects = TagManager()
    # essa variavel objects tem esse nome pq usamos Tag.objects.all() por exemplo.
    # se essa variavel se chamasse 'abc', usariamos Tag.abc.all() ou .active() ou qlqr coisa do tipo

    @python_2_unicode_compatible
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        view_name = "tags:detail"
        return reverse(view_name, kwargs={"slug": self.slug})


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    instance.title = instance.title.lower()
    if not instance.slug:
        instance.slug = slugify(instance.title)

pre_save.connect(tag_pre_save_receiver, sender=Tag)
