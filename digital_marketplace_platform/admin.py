from django.contrib import admin
from .models import Product, Order, OrderItem, BRFNUser

admin.site.register(BRFNUser)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(OrderItem)