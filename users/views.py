from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer, UserLikeSerializer
from drf_spectacular.utils import extend_schema
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
User = get_user_model()
success = "Amaliyot muvaffaqiyatli bajarildi"
error = "Xatolik yuz berdi"


# @extend_schema(responses=RegisterSerializer)
class RegisterApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("User created successfully", status=201)
        return Response(data="Malumotlar to'liq emas", status=400)


class ProfileEditApi(APIView):
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=200)
        return Response(data=error, status=200)


class LikeAddApi(APIView):
    serializer_class = UserLikeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UserLikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=200)
        return Response(data=serializer.errors, status=400)

