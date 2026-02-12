from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm


def order_create(request):
    """Оформление заказа"""
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    price=item['price'],
                    quantity=item['quantity'],
                )
            cart.clear()
            return render(request, 'orders/order_success.html', {'order': order})
    else:
        initial = {}
        if request.user.is_authenticated:
            initial = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'form': form,
    })


@login_required
def order_history(request):
    """История заказов"""
    orders = request.user.orders.all()
    return render(request, 'accounts/order_history.html', {'orders': orders})
