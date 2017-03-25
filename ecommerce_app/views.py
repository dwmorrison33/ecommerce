from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Product, Profile
from .forms import ProductForm

def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'home.html', {"products": products})

def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
            return render('/')
    return render(request, 'product_detail.html', {"product": product})

@login_required(login_url="/")
def create_product(request):
    error = ''
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect('my_products')
        else:
            error = "Data is not valid"

    product_form = ProductForm()
    return render(request, 'create_product.html', {"error": error})

@login_required(login_url="/")
def edit_product(request, id):
    try:
        product = Product.objects.get(id=id, user=request.user)
        error = ''
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance=product)
            if product_form.is_valid():
                product.save()
                return redirect('my_products')
            else:
                error = "Data is not valid"

        return render(request, 'edit_product.html', {"product": product, "error": error})
    except Product.DoesNotExist:
        return redirect('/')
    
@login_required(login_url="/")
def my_products(request):
    products = Product.objects.filter(user=request.user)
    return render(request, 'my_products.html', {"products": products})

@login_required(login_url="/")
def profile(request, username):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        profile.about = request.POST['about']
        profile.slogan = request.POST['slogan']
        profile.save()
    else:
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return redirect('/')

    products = Product.objects.filter(user=profile.user, status=True)
    return render(request, 'profile.html', {"profile": profile, "products": products})

