from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import UserVerification
from django.utils import timezone
from .serializers import UserSerializer, RegisterSerializer, UserLikeSerializer, UserBucketSerializer, \
    UserVerificationSerializer
from rest_framework.permissions import IsAuthenticated
from ProductsApp.serializers import ProductGetSerializer
from utils.imports import *


class RegisterApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        request.data['smsCode'] = 1111
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.data['username']).first()
            if user:
                raise ValidationError("Bu username avval foydalanilgan")
            serializer.save()
            return Response(data={"Tasdiqlash code jonatildi"}, status=200)
        return Response(data=serializer.errors, status=400)

        # serializer = RegisterSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response("User created successfully", status=201)
        # return Response(data="Malumotlar to'liq emas", status=400)


class UserVerificationApi(APIView):
    serializer_class = UserVerificationSerializer

    def post(self, request):
        user = UserVerification.objects.filter(**request.data).last()
        if user:
            if timezone.now() - user.datetime > timedelta(minutes=5):
                return Response(data="Sms code amal qilish muddati tugadi", status=400)
            User.objects.create_user(username=user.username, password=request.data['password'])
            UserVerification.objects.filter(username=request.data['username'], password=request.data['password']).delete()
            return Response(data="Foydalanuvchi muvaffaqiyatli yaratild", status=200)
        return Response(data="Bunday foydalanuvchi topilmadi", status=400)


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
            if value:
                if attr == "username":
                    if request.user.username != value:
                        if User.objects.filter(username=value).first():
                            raise ValidationError("Bunday username avval foydalanilgan")
                        setattr(request.user, attr, value)
                else:
                    setattr(request.user, attr, value)
        if password:
            request.user.set_password(password)
        request.user.save()
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
        serializer = ProductGetSerializer(data, many=True, context={'request': request})
        return Response(serializer.data, status=200)

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