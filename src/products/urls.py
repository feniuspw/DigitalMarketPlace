from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import (
    ProductCreateView,
    ProductDetailView,
    ProductDownloadView,
    ProductListView,
    ProductUpdateView,
    ProductRatingAjaxView,
    VendorListView
    )

app_name = 'products'
urlpatterns = [
    # url(r'^$', views.detail_view, name='detail_view'),
    # ex: /product/detail/5
    # \d+ only digits
    # parameter name = object_id
    # .* everything
    # url(r'^create/$', views.create_view, name='create_view'),
    # url(r'^detail/(?P<object_id>\d+)/$', views.detail_view, name='detail_view'),
    # url(r'^detail/(?P<slug>[\w-]+)/$', views.detail_slug_view, name='detail_slug_view'),
    # url(r'^detail/(?P<object_id>\d+)/edit/$', views.update_view, name='update_view'),
    url(r'^list/$', ProductListView.as_view(), name='list'),
    # vendor_name eh passado como **kwargs
    url(r'^vendor/$', RedirectView.as_view(pattern_name='products:list'), name='vendor_list'),
    url(r'^vendor/(?P<vendor_name>[\w.@+-]+)/$', VendorListView.as_view(), name='vendor_detail'),

    url(r'^detail/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^detail/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),

    url(r'^(?P<pk>\d+)/download/$', ProductDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', ProductDownloadView.as_view(), name='download_slug'),

    url(r'^detail/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='update'),
    url(r'^detail/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update_slug'),

    url(r'^ajax/rating/$', ProductRatingAjaxView.as_view(), name='ajax_rating'),


]
