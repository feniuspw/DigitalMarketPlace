from django.conf.urls import url

from .views import (
    TagListView,
    TagDetailView
    )

app_name = 'products'
urlpatterns = [
    url(r'^list/$', TagListView.as_view(), name='list '),
    url(r'^detail/(?P<slug>[\w-]+)/$', TagDetailView.as_view(), name='detail'),
]
