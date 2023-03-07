from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=300, null=True, blank=True)
    phone = models.IntegerField(max_length=11, null=False)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_name = models.CharField(max_length=30)
    product_desc = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.product_name


class Vendor(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=300, null=True, blank=True)
    phone = models.IntegerField(max_length=11, null=False)
    address = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Product_holders_List(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='set_vendor')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='set_product')
    price = models.IntegerField(null=False)
    stock = models.IntegerField(null=False, default=0)


class Order(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='set_user')
    quantity = models.IntegerField(null=False, default=1)
    total_price = models.IntegerField()

    def __int__(self):
        return self.Order.pk
