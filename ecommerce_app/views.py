from django.shortcuts import render, redirect
from .models import Product

def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'home.html', {"products": products})

def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
            return render('/')
    return render(request, 'product_detail.html', {"product": product})