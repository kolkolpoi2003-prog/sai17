from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class UserProfile(models.Model):
    """Профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    phone = models.CharField('Телефон', max_length=20, blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    address = models.TextField('Адрес', blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/', blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль {self.user.username}"


class Wishlist(models.Model):
    """Избранное"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist', verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    created = models.DateTimeField('Добавлен', auto_now_add=True)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ['user', 'product']

    def __str__(self):
        return f"{self.user.username} — {self.product.name}"
