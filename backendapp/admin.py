from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Category, Brand, Product, Cart, CartProduct, Order, Review

# Register your models here.
admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Order)
admin.site.register(Review)
