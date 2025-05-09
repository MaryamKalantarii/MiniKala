from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'total_price']
    can_delete = False

    def total_price(self, obj):
        return obj.total_price
    total_price.short_description = 'Total Price'

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'total_items', 'total', 'created_date']
    readonly_fields = ['created_date', 'total', 'total_items']
    inlines = [CartItemInline]
    search_fields = ['user__email']

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price']
    search_fields = ['product__title', 'cart__user__email']
    readonly_fields = ['total_price']

