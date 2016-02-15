from django.conf.urls import url

from .views import (
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    )
from . import views

app_name = 'products'
urlpatterns = [
    # ex: /polls/
    # url(r'^$', views.detail_view, name='detail_view'),
    # ex: /product/detail/5
    # \d+ only digits
    # parameter name = object_id
    # .* everything
    # url(r'^create/$', views.create_view, name='create_view'),
    url(r'^detail/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='product_detail_view'),
    url(r'^detail/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='product_detail_slug_view'),
    # url(r'^detail/(?P<object_id>\d+)/$', views.detail_view, name='detail_view'),
    # url(r'^detail/(?P<slug>[\w-]+)/$', views.detail_slug_view, name='detail_slug_view'),
    # url(r'^detail/(?P<object_id>\d+)/edit/$', views.update_view, name='update_view'),
    url(r'^detail/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='product_update_view'),
    url(r'^detail/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='product_update_slug_view'),
    url(r'^list/', ProductListView.as_view(), name='product_list_view'),
    url(r'^add/$', ProductCreateView.as_view(), name="product_create_view"),

]
