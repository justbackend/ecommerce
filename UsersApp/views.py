import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, timedelta
from .models import UserVerification, Recovery
from django.utils import timezone
from .serializers import UserSerializer, RegisterSerializer, UserLikeSerializer, UserBucketSerializer, \
    UserVerificationSerializer, RecoverPasswordSerializer, SetRecoveryPasswordSerializer
from rest_framework.permissions import IsAuthenticated
from ProductsApp.serializers import ProductGetSerializer
from utils.imports import *
from random import randint
sms_token = ""


def refresh_token():
    global sms_token
    url = "https://notify.eskiz.uz/api/auth/login"
    payload = {'email': 'izzatullaev2001abror@gmail.com',
               'password': 'Z7YaqztTs7NXs57IsYgVCdb0U2VfB0HyuhbD2rD4'}
    response = requests.request("POST", url, data=payload)
    if response.status_code == 200:
        sms_token = response.json()['data']['token']
        return sms_token




class RegisterApi(APIView):

    serializer_class = RegisterSerializer



    def post(self, request):
        global sms_token
        code = randint(123467, 987654)
        request.data['smsCode'] = code
        serializer = UserVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['username']
            user = User.objects.filter(username=phone_number).first()
            if user:
                raise ValidationError("Bu username avval foydalanilgan")
            url2 = "https://notify.eskiz.uz/api/message/sms/send"
            headers = {
                'Authorization': f'Bearer {sms_token}'
            }
            message = f"Telmee sayti uchun tasdiqlash ko'dingiz: {code}"
            payload = {'mobile_phone': phone_number,
                       'message': message,
                       'from': 'Telmee'}
            response = requests.post(url=url2, data=payload, headers=headers)
            if response.status_code != 200:
                sms_token = refresh_token()
                headers = {
                    'Authorization': f'Bearer {sms_token}'
                }
                response = requests.post(url=url2, data=payload, headers=headers)
            if response.status_code == 200:
                serializer.save()
                return Response(data={"Tasdiqlash code jonatildi"}, status=200)
            return Response(data=response, status=400)
        return Response(data=serializer.errors, status=400)


class UserVerificationApi(APIView):
    serializer_class = UserVerificationSerializer

    def post(self, request):
        user = UserVerification.objects.filter(**request.data).last()
        if user:
            if timezone.now() - user.datetime > timedelta(minutes=120):
                user.delete()
                return Response(data="Sms code amal qilish muddati tugadi", status=400)
            User.objects.create_user(username=user.username, password=request.data['password'])
            UserVerification.objects.filter(username=request.data['username'], password=request.data['password']).delete()
            return Response(data="Foydalanuvchi muvaffaqiyatli yaratild", status=200)
        return Response(data="Bunday foydalanuvchi topilmadi", status=400)


class RecoverPasswordApi(APIView):
    serializer_class = RecoverPasswordSerializer
    def post(self, request):
        global sms_token
        serializer = RecoverPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user = User.objects.filter(username=phone_number).first()
            if not user:
                raise ValidationError("Siz ro'yxatdan o'tmagansiz")
            code = randint(123467, 987654)
            request.data['smsCode'] = code
            url2 = "https://notify.eskiz.uz/api/message/sms/send"
            headers = {
                'Authorization': f'Bearer {sms_token}'
            }
            message = f"Telmee sayti uchun parol tiklash uchun kodingiz: {code}"
            payload = {'mobile_phone': phone_number,
                       'message': message,
                       'from': 'Telmee'}
            response = requests.post(url=url2, data=payload, headers=headers)
            if response.status_code != 200:
                sms_token = refresh_token()
                headers = {
                    'Authorization': f'Bearer {sms_token}'
                }
                response = requests.post(url=url2, data=payload, headers=headers)
            if response.status_code == 200:
                Recovery.objects.create(phone_number=phone_number, code=code)
                return Response("Sms code muvaffaqiyatli yuborildi", 200)
            return Response(response, 400)

    def put(self, request):
        serializer = RecoverPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data.get('code', None)
            if code is None:
                raise CustomException("Code kiritilmagan")
            recover = Recovery.objects.filter(phone_number=phone_number, code=code).first()
            if recover:
                return Response(data="Foydalanuvchi parolni yangilash uchun tasdiqlandi", status=200)
            raise CustomException("Notog'ri ko'd kiritildi")
        raise CustomException(serializer.errors)


class SetRecoveryPasswordApi(APIView):
    serializer_class = SetRecoveryPasswordSerializer
    def post(self, request):
        serializer = SetRecoveryPasswordSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            password = serializer.validated_data['password']
            recover = Recovery.objects.filter(phone_number=phone_number, code=code).first()
            if not recover:
                raise CustomException("Xatolik yuz berdi")
            user = User.objects.filter(username=phone_number).first()
            user.set_password(password)
            user.save()
            recover.delete()
            return Response(success, 200)
        raise CustomException(serializer.errors)


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