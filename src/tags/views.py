from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Tag
from analytics.models import TagView
# Create your views here.


class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, *args, **kwargs):
        context = super(TagDetailView, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated():
            # self.get_object() gets the instance that is been called in the DetailView specifically
            tag = self.get_object()
            new_view = TagView.objects.add_count(self.request.user, tag)
        return context


class TagListView(ListView):
    model = Tag

    # dessa forma limita o que vai puxar no list.
    # existe uma forma de fazer isso automaticamente. que é nas models, (classe TagManager)
    # def get_queryset(self):
    #     return Tag.objects.all().active()
    # esse metodo sobrescreve o padrao (que busca todos os objetos do banco automaticamente.
    # dai vc pode fazer o que quiser ao inves de puxar todos

