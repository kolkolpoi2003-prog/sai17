from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class Category(models.Model):
    """Категории товаров: Солнцезащитные очки, Оправы, Линзы и т.д."""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    image = models.ImageField('Изображение', upload_to='categories/', blank=True)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Бренды: Ray-Ban, Oakley, Acuvue и т.д."""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', max_length=200, unique=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True)
    description = models.TextField('Описание', blank=True)
    is_active = models.BooleanField('Активен', default=True)

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Основная модель товара"""

    class Status(models.TextChoices):
        AVAILABLE = 'available', 'В наличии'
        OUT_OF_STOCK = 'out_of_stock', 'Нет в наличии'
        PREORDER = 'preorder', 'Предзаказ'

    name = models.CharField('Название', max_length=300)
    slug = models.SlugField('URL', max_length=300, unique=True)
    sku = models.CharField('Артикул', max_length=50, unique=True, default=uuid.uuid4)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='products',
        verbose_name='Бренд'
    )
    description = models.TextField('Описание', blank=True)
    specifications = models.JSONField('Характеристики', default=dict, blank=True,
                                      help_text='JSON: {"Материал оправы": "Металл", "Тип линз": "Поляризованные"}')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    old_price = models.DecimalField('Старая цена', max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField('Статус', max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    is_hit = models.BooleanField('Хит продаж', default=False)
    is_new = models.BooleanField('Новинка', default=False)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлён', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category']),
            models.Index(fields=['is_hit']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    @property
    def discount_percent(self):
        """Процент скидки"""
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    @property
    def is_on_sale(self):
        return self.old_price is not None and self.old_price > self.price

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE

    @property
    def main_image(self):
        img = self.images.filter(is_main=True).first()
        if not img:
            img = self.images.first()
        return img

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Изображения товара"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Товар'
    )
    image = models.ImageField('Изображение', upload_to='products/')
    alt = models.CharField('Alt текст', max_length=200, blank=True)
    is_main = models.BooleanField('Главное', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
        ordering = ['order']

    def __str__(self):
        return f"Фото {self.product.name} #{self.order}"


class Review(models.Model):
    """Отзывы о товарах"""
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Товар'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    rating = models.PositiveIntegerField(
        'Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField('Текст отзыва')
    created = models.DateTimeField('Дата', auto_now_add=True)
    is_approved = models.BooleanField('Одобрен', default=False)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"Отзыв {self.user.username} на {self.product.name}"


class PromoCode(models.Model):
    """Промокоды"""
    code = models.CharField('Код', max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(
        'Скидка %',
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    is_active = models.BooleanField('Активен', default=True)
    valid_from = models.DateTimeField('Действует с')
    valid_to = models.DateTimeField('Действует до')
    usage_limit = models.PositiveIntegerField('Лимит использований', default=0, help_text='0 = без лимита')
    times_used = models.PositiveIntegerField('Использован раз', default=0)

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return f"{self.code} (-{self.discount_percent}%)"

    @property
    def is_valid(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_to:
            return False
        if self.usage_limit > 0 and self.times_used >= self.usage_limit:
            return False
        return True
