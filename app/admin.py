from django.contrib import admin
from .models import (
    Customer, Product, Cart, OrderPlaced,Payment
)

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'village', 'city', 'state','union']


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'brand', 'category', 'product_image']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'status']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'payment_method', 'transaction_id')
    search_fields = ('customer_name', 'transaction_id')
    list_filter = ('payment_method',)
    ordering = ('customer_name',)
