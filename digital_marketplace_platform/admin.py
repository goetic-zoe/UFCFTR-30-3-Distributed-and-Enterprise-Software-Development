from django.contrib import admin
from .models import Producer, Product, Order, Customer, OrderItem

admin.site.register(Producer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Customer)
admin.site.register(OrderItem)