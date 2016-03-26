from django.conf.urls import url

from .views import (
    SellerDashboard,
)

app_name = 'sellers'

urlpatterns = [
    url(r'^/$', SellerDashboard.as_view(), name='dashboard'),
]
