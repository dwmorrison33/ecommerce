from django.contrib import admin
from .models import Profile, Product, Purchase, Review

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Review)