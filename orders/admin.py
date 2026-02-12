from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'product_name', 'price', 'quantity']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'city', 'status', 'created']
    list_filter = ['status', 'created']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_editable = ['status']
    inlines = [OrderItemInline]
