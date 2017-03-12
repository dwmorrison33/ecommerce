from django.conf.urls import url
from ecommerce_app import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^products/(?P<id>[0-9]+)/$', views.product_detail, name='product_detail'),
]