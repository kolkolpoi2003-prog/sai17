from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Review, PromoCode


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt', 'is_main', 'order']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'order', 'is_active']
    list_filter = ['is_active', 'parent']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'price', 'old_price', 'status', 'is_hit', 'is_new']
    list_filter = ['status', 'category', 'brand', 'is_hit', 'is_new']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'status', 'is_hit', 'is_new']
    inlines = [ProductImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'sku', 'category', 'brand')
        }),
        ('Цены', {
            'fields': ('price', 'old_price')
        }),
        ('Описание', {
            'fields': ('description', 'specifications')
        }),
        ('Статус', {
            'fields': ('status', 'is_hit', 'is_new')
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created']
    list_filter = ['is_approved', 'rating']
    list_editable = ['is_approved']


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'is_active', 'valid_from', 'valid_to', 'times_used']
    list_filter = ['is_active']
    list_editable = ['is_active']
