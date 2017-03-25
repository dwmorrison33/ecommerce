from django.conf.urls import url
from ecommerce_app import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^products/(?P<id>[0-9]+)/$', views.product_detail, name='product_detail'),
    url(r'^my_products/$', views.my_products, name='my_products'),
    url(r'^create_product/$', views.create_product, name='create_product'),
    url(r'^edit_product/(?P<id>[0-9]+)/$', views.edit_product, name='edit_product'),
    url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
]