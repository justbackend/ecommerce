from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, UserLikeSerializer, UserBucketSerializer
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError, ErrorDetail
from rest_framework.permissions import IsAuthenticated
from ProductsApp.serializers import ProductGetSerializer
User = get_user_model()
success = "Amaliyot muvaffaqiyatli bajarildi"
error = "Xatolik yuz berdi"
none = "Kiritilganlar bo'yicha malumot topilmadi"
value_e = "Malumotlarni to'g'ri shakilda jo'nating"

# @extend_schema(responses=RegisterSerializer)
class RegisterApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User created successfully", status=201)
        return Response(data="Malumotlar to'liq emas", status=400)


class UserApi(APIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=200)
        # return Response(data=serializer.errors, status=400)

    def put(self, request):
        password = request.data.pop('password')
        for attr, value in request.data.items():
            setattr(request.user, attr, value)
        request.user.save()
        request.user.set_password(password)
        return Response(data=success, status=200)



# class ProfileEditApi(APIView):
#     serializer_class = UserSerializer
#     # permission_classes = [IsAuthenticated]






class LikeAddApi(APIView):
    serializer_class = UserLikeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.user.likedProducts.all()
        serializer = ProductGetSerializer(data, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = UserLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=200)
        return Response(data=serializer.errors, status=400)

    def delete(self, request):
        product_id = request.data.get('product_id', None)
        if product_id:
            product = request.user.likedProducts.filter(id=product_id)
            if product:
                product.delete()
                return Response(data=success, status=200)
            return Response(data=none, status=400)
        return Response(data=value_e, status=400)


class BucketAddApi(APIView):
    serializer_class = UserBucketSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = request.user.bucket.all()
        return Response(data, status=200)

    def post(self, request):
        serializer = UserBucketSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=200)
        return Response(data=serializer.errors, status=400)

    def delete(self, request):
        product_id = request.data.get('product_id', None)
        if product_id:
            product = request.user.bucket.filter(id=product_id)
            if product:
                product.delete()
                return Response(data=success, status=200)
            return Response(data=none, status=400)
        return Response(data=value_e, status=400)