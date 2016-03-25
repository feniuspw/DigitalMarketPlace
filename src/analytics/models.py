from django.conf import settings
from django.db import models

# Create your models here.
from tags.models import Tag
from django.utils.encoding import python_2_unicode_compatible


class TagViewManager(models.Manager):
    def add_count(self, user, tag):
        obj, created = self.model.objects.get_or_create(user=user, tag=tag)
        obj.count += 1
        obj.save()
        return obj


class TagView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    tag = models.ForeignKey(Tag)
    count = models.IntegerField(default=0)

    objects = TagViewManager()

    @python_2_unicode_compatible
    def __str__(self):
        return str(self.tag.title)




