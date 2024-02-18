from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets

from products.models import Product

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'realUsername']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def save(self, **kwargs):
        try:
            phone_number1 = self.validated_data.get('username', None)
            password = self.validated_data['password']

            if phone_number1 and User.objects.filter(username=phone_number1).exists():
                raise ValidationError(detail="Bu telefon raqam ro'yhatdan o'tgan")

            User.objects.create_user(username=phone_number1, password=password)
            return Response("User created successfully", status=201)
        except IntegrityError as e:
            return Response({"error": str(e)}, status=400)


class UserLikeSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        product = Product.objects.filter(id=self.validated_data["product_id"]).first()
        if product is None:
            raise ValidationError(detail="Bunday product mavjud emas")
        self.context['request'].user.likedProducts.add(product)
        return product




