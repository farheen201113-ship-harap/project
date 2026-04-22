from django.contrib import admin
from .models import Customer, Product, Cart, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'phone', 'created_at']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-created_at']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'original_price', 'rating', 'in_stock', 'is_new', 'created_at']
    search_fields = ['name', 'category', 'processor', 'os']
    list_filter = ['category', 'is_new', 'is_assured', 'in_stock', 'emi_available']
    list_editable = ['price', 'in_stock', 'is_new']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category', 'price', 'original_price', 'image')
        }),
        ('Specifications', {
            'fields': ('processor', 'ram', 'storage', 'display', 'graphics', 'battery', 'os', 'weight')
        }),
        ('Features & Ratings', {
            'fields': ('features', 'rating', 'rating_count')
        }),
        ('Badges & Stock', {
            'fields': ('is_new', 'is_assured', 'in_stock', 'stock_count')
        }),
        ('Delivery & Offers', {
            'fields': ('free_delivery', 'delivery_text', 'emi_available', 'emi_text', 'offer_text')
        }),
    )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer', 'first_name', 'mobile', 'total_amount', 'payment_method', 'status', 'created_at']
    search_fields = ['order_id', 'mobile', 'first_name']
    ordering = ['-created_at']