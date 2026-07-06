from django.contrib.auth.models import AbstractUser

from django.db import models

class BRFNUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('producer', 'Producer'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='brfnuser_set'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='brfnuser_set'
    )

    def __str__(self):
        return self.username

class Product(models.Model):
    producer = models.ForeignKey(BRFNUser, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability_start = models.DateField()
    availability_end = models.DateField()

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey('BRFNUser', related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
