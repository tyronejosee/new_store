"""Views for Cart App."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from cart.models import Cart


@login_required
def cart(request):
    """Render the cart view."""
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    products = cart.products.all()
    return render(request, "cart/cart_list.html", {'products': products, 'cart': cart})


@login_required
def add_product(request, product_id):
    """Add a product to the cart."""
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart.add_product(product)
    return redirect("users:cart")


@login_required
def remove_product(request, product_id):
    """Remove a product from the cart."""
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart.remove_product(product)
    return redirect("users:cart")


@login_required
def subtract_product(request, product_id):
    """Subtract a product from the cart."""
    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user)
    cart.subtract_product(product)
    return redirect("users:cart")


@login_required
def clear_cart(request):
    """Clear the cart."""
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart.clear_cart()
    return redirect("users:cart")
