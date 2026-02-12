from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    """Добавить товар в корзину (AJAX)"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # BUGFIX: Validate quantity to prevent ValueError crash on invalid input
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity < 1:
            quantity = 1
        if quantity > 99:
            quantity = 99
    except (ValueError, TypeError):
        quantity = 1
    override = request.POST.get('override', False) == 'true'
    cart.add(product=product, quantity=quantity, override_quantity=override)
    return JsonResponse({
        'status': 'ok',
        'total_items': len(cart),
        'total_price': str(cart.get_total_price()),
    })


@require_POST
def cart_remove(request, product_id):
    """Удалить товар из корзины (AJAX)"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({
        'status': 'ok',
        'total_items': len(cart),
        'total_price': str(cart.get_total_price()),
    })


@require_POST
def cart_update(request, product_id):
    """Обновить количество товара (AJAX)"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    # BUGFIX: Validate quantity to prevent ValueError crash
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 99:
            quantity = 99
    except (ValueError, TypeError):
        quantity = 1
    if quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
    else:
        cart.remove(product)
    return JsonResponse({
        'status': 'ok',
        'total_items': len(cart),
        'total_price': str(cart.get_total_price()),
    })


def cart_detail(request):
    """Страница корзины"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
