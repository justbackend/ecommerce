from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# from ProductsApp.models import Product


class CustomUser(AbstractUser):
    realUsername = models.CharField(max_length=32)
    likedProducts = models.ManyToManyField('ProductsApp.Product', related_name="likedBy",)
    bucket = models.ManyToManyField('ProductsApp.Product', related_name="storedBy")


class UserVerification(models.Model):
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    smsCode = models.IntegerField()
    datetime = models.DateTimeField(auto_now_add=True)
