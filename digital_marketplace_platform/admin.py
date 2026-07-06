from django.contrib import admin
from .models import Product, Order, OrderItem, User

admin.site.register(User)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)