from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Product, Cart
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('product')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def product(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})


@login_required
def addToCart(request, product_id):
    # product = Product.objects.get(id=product_id)  # selected product with id
    # Check if the product is already in the user's cart
    # cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    # if not created:  # If the product already exists in the cart, increase the quantity
    #     cart_item.quantity += 1
    #     cart_item.save()
    # return redirect('view_cart')
    product = Product.objects.get(id=product_id)
    cart_item = Cart.objects.filter(user=request.user, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(user=request.user, product=product, quantity=1)

    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)  # Get all cart items for the logged-in user
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def remove(request, item_id):
    # try:
    #     # Get the cart item to be removed
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()  # Remove the item from the cart
        return redirect('view_cart')
    # except Cart.DoesNotExist:
    #     pass  # If the item doesn't exist, do nothing

    # return redirect('view_cart')