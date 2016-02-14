from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    # ex: /polls/
    # url(r'^$', views.detail_view, name='detail_view'),
    # ex: /product/detail/5
    # \d+ only digits
    # parameter name = object_id
    # .* everything
    url(r'^create/$', views.create_view, name='create_view'),
    url(r'^detail/(?P<object_id>\d+)', views.detail_view, name='detail_view'),
    url(r'^detail/(?P<slug>[\w-]+)', views.detail_slug_view, name='detail_slug_view'),
    url(r'^list/', views.list_view, name='list_view'),
]
