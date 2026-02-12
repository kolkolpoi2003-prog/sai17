from django.contrib import admin
from .models import UserProfile, Wishlist


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city']
    search_fields = ['user__username', 'phone']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created']
    list_filter = ['created']
