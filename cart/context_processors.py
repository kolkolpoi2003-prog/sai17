from .cart import Cart


def cart(request):
    """Глобальный доступ к корзине в шаблонах"""
    return {'cart': Cart(request)}
