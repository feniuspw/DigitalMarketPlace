from django.conf.urls import url

from products.views import (
    ProductCreateView,
    SellerProductListView,
    ProductUpdateView,
)

from .views import (
    SellerDashboard,
    SellerTransactionListView,
    SellerProductDetailRedirectView,
)

app_name = 'sellers'

urlpatterns = [
    url(r'^$', SellerDashboard.as_view(), name='dashboard'),
    url(r'^transaction/$', SellerTransactionListView.as_view(), name='transactions'),
    url(r'^product/add/$', ProductCreateView.as_view(), name="product_create"),
    url(r'^product/$', SellerProductListView.as_view(), name="product_list"),
    url(r'^product/(?P<pk>\d+)/edit/$', ProductUpdateView.as_view(), name='product_edit'),
    url(r'^product/(?P<pk>\d+)/$', SellerProductDetailRedirectView.as_view()),
]
