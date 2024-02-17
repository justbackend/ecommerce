from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from .models import User
from django.db import IntegrityError


class RegisterApi(APIView):
    def post(self, request):
        try:
            username = request.data['phoneNumber']
            real_username = request.data['username']
            password = request.data['password']
            if User.objects.filter(real_username=real_username).exists():
                return Response("Bu username ro'yhatdan o'tgan", status=400)
            User.objects.create_user(username=username, real_username=real_username, password=password)
            return Response("User created successfully", status=201)
        except IntegrityError as e:
            return Response({"error": str(e)}, status=400)


class ProfileEditApi(APIView):
    def put(self, request):
        name = request.data.get('name', None)
        last_name = request.data.get('surname', None)
        gmail = request.data.get('gmail', None)
        password = request.data.get('password', None)
        phone_number = request.data.get('phoneNumber', None)

        if User.objects.filter(email=gmail).exists():
            return Response("Bu email oldin ro'yxatdan o'tgan", status=403)
        elif User.objects.filter(username=phone_number).exists():
            return Response("Bu telefon raqam avval ro'yxatdan o'tkazilgan", status=403)
        else:
            try:
                User.objects.filter(pk=request.user.id).update()


