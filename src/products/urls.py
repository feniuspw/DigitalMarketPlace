from django.conf.urls import url

from .views import (
    ProductCreateView,
    ProductDetailView,
    ProductDownloadView,
    ProductListView,
    ProductUpdateView,
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
    url(r'^detail/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='detail'),
    url(r'^detail/(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail_slug'),

    url(r'^(?P<pk>\d+)/download/$', ProductDownloadView.as_view(), name='download'),
    url(r'^(?P<slug>[\w-]+)/download/$', ProductDownloadView.as_view(), name='download_slug'),

    url(r'^detail/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='update'),
    url(r'^detail/(?P<slug>[\w-]+)/edit/$', ProductUpdateView.as_view(), name='update_slug'),

    url(r'^list/$', ProductListView.as_view(), name='list '),
    url(r'^add/$', ProductCreateView.as_view(), name="create"),

]
