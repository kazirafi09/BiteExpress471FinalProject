from django.contrib import admin

# Register your models here.
from .models import Order, Review, CartItem, Cart, OrderItem
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(OrderItem)