from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)
    price = models.IntegerField()
    inventory = models.IntegerField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateField()
    def __str__(self):
        return self.name


class Transaction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller_users")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer_user")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.IntegerField()
    total = models.IntegerField()
    pay_time = models.DateTimeField()


class Comment(models.Model):
    content = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    post_time = models.DateField()