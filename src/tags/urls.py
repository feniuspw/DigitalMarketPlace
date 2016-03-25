from django.conf.urls import url

from .views import (
    TagListView,
    TagDetailView
    )

app_name = 'tags'
urlpatterns = [
    url(r'^detail/(?P<slug>[\w-]+)/$', TagDetailView.as_view(), name='detail'),
    url(r'^list/$', TagListView.as_view(), name='list'),
]
