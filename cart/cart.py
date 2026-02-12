from decimal import Decimal, InvalidOperation
from django.conf import settings
from shop.models import Product


class Cart:
    """Корзина на основе сессий Django"""

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price),
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        # Map loaded products to cart items
        product_map = {str(p.id): p for p in products}

        # BUGFIX: Clean up stale cart entries for deleted products
        stale_ids = [pid for pid in cart if pid not in product_map]
        if stale_ids:
            for pid in stale_ids:
                del self.cart[pid]
            self.save()

        for product_id, item in cart.items():
            if product_id in product_map:
                item['product'] = product_map[product_id]
                try:
                    item['price'] = Decimal(item['price'])
                except (InvalidOperation, ValueError):
                    item['price'] = product_map[product_id].price
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0')
        for item in self.cart.values():
            try:
                price = Decimal(item['price'])
            except (InvalidOperation, ValueError):
                price = Decimal('0')
            total += price * item['quantity']
        return total

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
