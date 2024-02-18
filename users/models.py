from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
# from products.models import Product


class CustomUser(AbstractUser):
    realUsername = models.CharField(max_length=32)
    likedProducts = models.ManyToManyField('products.Product', related_name="likedBy")
    bucket = models.ManyToManyField('products.Product', related_name="storedBy")


