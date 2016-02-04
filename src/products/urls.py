from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    # ex: /polls/
    # url(r'^$', views.detail_view, name='detail_view'),
    # ex: /product/detail/
    url(r'detail/', views.detail_view, name='detail_view'),
    url(r'list/', views.list_view, name='list_view'),
]
