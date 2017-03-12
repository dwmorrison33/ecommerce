from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {})

def product_detail(request, id):
    return render(request, 'product_detail.html', {})