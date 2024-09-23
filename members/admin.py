from django.contrib import admin
from .models import Buyer, Restaurant, Deliveryman, FoodItem
admin.site.register(Buyer)
admin.site.register(Restaurant)
admin.site.register(Deliveryman)
admin.site.register(FoodItem)