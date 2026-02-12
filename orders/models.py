from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    """Заказ"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Ожидает обработки'
        PROCESSING = 'processing', 'В обработке'
        SHIPPED = 'shipped', 'Отправлен'
        DELIVERED = 'delivered', 'Доставлен'
        CANCELLED = 'cancelled', 'Отменён'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='orders',
        verbose_name='Пользователь'
    )
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    email = models.EmailField('Email')
    phone = models.CharField('Телефон', max_length=20)
    city = models.CharField('Город', max_length=100)
    address = models.TextField('Адрес доставки')
    postal_code = models.CharField('Почтовый индекс', max_length=20, blank=True)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.PENDING)
    promo_code = models.CharField('Промокод', max_length=50, blank=True)
    discount = models.DecimalField('Скидка', max_digits=10, decimal_places=2, default=0)
    notes = models.TextField('Комментарий', blank=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return f"Заказ #{self.id}"

    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        return total - self.discount


class OrderItem(models.Model):
    """Позиция в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(
        'shop.Product', on_delete=models.SET_NULL,
        null=True, verbose_name='Товар'
    )
    product_name = models.CharField('Название товара', max_length=300)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f"{self.product_name} x{self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
