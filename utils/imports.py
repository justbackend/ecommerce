from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
User = get_user_model()
success = "Amaliyot muvaffaqiyatli bajarildi"
error = "Xatolik yuz berdi"
none = "Kiritilganlar bo'yicha malumot topilmadi"
value_e = "Malumotlarni to'g'ri shakilda jo'nating"
