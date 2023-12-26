from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    gender_choices = [('M', 'Male'),
                      ('F', 'Female'),
                      ('O', 'Others')]

    user_id = models.OneToOneField(to=User, related_name='customer', on_delete=models.CASCADE)

    name = models.CharField(max_length=75, null=False, blank=False)     # Required Field
    email = models.EmailField(blank=False, null=False, unique=True)     # Required Field
    dob = models.DateField(blank=False, null=False)     # Required Field
    gender = models.CharField(max_length=1, choices=gender_choices, blank=False, null=False)     # Required Field
    phone = models.CharField(max_length=10, null=True)     # Optional Field
    address = models.TextField(null=True)     # Optional Field
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'customer'

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    name = models.CharField(max_length=75, blank=False, null=False, unique=True)     # Required Field

    class Meta:
        db_table = 'category'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)     # Required Field
    description = models.TextField(null=True)     # Optional Field
    category_id = models.ForeignKey(to=Category, on_delete=models.RESTRICT, related_name='products')
    price = models.PositiveIntegerField(null=False, blank=False)     # Required Field
    is_available = models.BooleanField(default=True)     # optional Field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'product'
        ordering = ['created_at']


class Cart(models.Model):
    customer_id = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='my_cart')
    product_id = models.ForeignKey(to=Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)     # Optional Field

    class Meta:
        db_table = 'cart'


class Orders(models.Model):
    customer_id = models.ForeignKey(to=Customer, on_delete=models.RESTRICT, related_name='my_orders')
    product_id = models.ForeignKey(to=Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(null=False, blank=False)    # Required Field
    subtotal = models.PositiveIntegerField(null=False, blank=False)    # Required Field
    placed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'orders'