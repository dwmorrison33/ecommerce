from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Product, Profile, Purchase, Review
from .forms import ProductForm

from django.conf import settings

import braintree

braintree.Configuration.configure(braintree.Environment.Sandbox,
                                    merchant_id=settings.BRAINTREE_MERCHANT_ID,
                                    public_key=settings.BRAINTREE_PUBLIC_KEY,
                                    private_key=settings.BRAINTREE_PRIVATE_KEY)


def home(request):
    products = Product.objects.filter(status=True)
    return render(request, 'home.html', {"products": products})

def product_detail(request, id):
    if request.method =='POST' and \
        not request.user.is_anonymous() and \
        Purchase.objects.filter(product_id=id, buyer=request.user).count() > 0 and \
        'content' in request.POST and \
        request.POST['content'].strip() != '':
        Review.objects.create(content=request.POST['content'], 
                              product_id=id, 
                              user=request.user)

    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
            return render('/')

    if request.user.is_anonymous() or \
        Purchase.objects.filter(product=product, buyer=request.user).count() == 0 or \
        Review.objects.filter(product=product, user=request.user).count() > 0:
        show_post_review = False
    else:
        show_post_review = Purchase.objects.filter(product=product, buyer=request.user).count() > 0

    reviews = Review.objects.filter(product=product)
    client_token = braintree.ClientToken.generate()

    return render(request, 'product_detail.html', {"show_post_review": show_post_review,
                                                   "product": product,
                                                   "client_token": client_token,
                                                   "reviews": reviews})

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

@login_required(login_url="/")
def create_purchase(request):
    if request.method == 'POST':
        try:
            product = Product.objects.get(id = request.POST['product_id'])
        except Product.DoesNotExist:
            return redirect('/')

        nonce = request.POST["payment_method_nonce"]
        result = braintree.Transaction.sale({
            "amount": product.price,
            "payment_method_nonce": nonce
        })

        if result.is_success:
            #messages.success(request, "You successfully purchased this product")
            Purchase.objects.create(product=product, buyer=request.user)

    return redirect('/')

@login_required(login_url="/")
def products_bought(request):
    purchases = Purchase.objects.filter(product__user=request.user)
    return render(request, 'products_bought.html', {"purchases": purchases})

@login_required(login_url="/")
def products_sold(request):
    purchases = Purchase.objects.filter(buyer=request.user)
    return render(request, 'products_sold.html', {"purchases": purchases})

def category(request, link):

    categories = {
        "electronics": "EL",
        "collectibles": "CO",
        "finance": "FI",
        "home": "HO",
        "travel": "TR"
    }

    try:
        products = Product.objects.filter(category=categories[link])
        return render(request, 'home.html', {"products": products})
    except KeyError:
        return redirect('home')

def search(request):
    products = Product.objects.filter(title__contains=request.GET['title'])
    return render(request, 'home.html', {"products": products})