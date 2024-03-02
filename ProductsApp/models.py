from django.contrib.auth import get_user_model
from django.db import models
# from UsersApp.models import CustomUser
User = get_user_model()


class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product', db_index=True)
    phoneName = models.CharField(max_length=250, db_index=True)
    phoneMarka = models.CharField(max_length=50)
    cost = models.FloatField()
    costType = models.CharField(max_length=10)
    phoneMemory = models.CharField(max_length=30)
    phoneColor = models.CharField(max_length=20)
    document = models.BooleanField(default=False)
    isNew = models.BooleanField(default=False)
    comment = models.TextField()
    adress = models.TextField()
    phoneNumber = models.CharField(max_length=15)
    time = models.DateTimeField(auto_now_add=True)


class Views(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views', db_index=True)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', db_index=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', db_index=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')

