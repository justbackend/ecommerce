from utils.imports import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Views, Likes
from .serializers import ProductSerializer, ImageSerializer, ProductGetSerializer, ProductIdSerializer
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, Http404, HttpResponseServerError
success = "Amaliyot muvaffaqiyatli bajarildi"
error = "Xatolik yuz berdi"
none = "Kiritilganlar bo'yicha malumot topilmadi"
value_e = "Malumotlarni to'g'ri shakilda jo'nating"

def get_product(product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise CustomException(detail=none)

    return product


class CreateProductApi(APIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=201)
        return Response(data=serializer.errors, status=400)

    def get(self, request):
        products = request.user.product.all()
        serializer = ProductGetSerializer(products, many=True, context={"request": request})
        return Response(data=serializer.data, status=200)

    def delete(self, request):
        product_id = request.query_params.get('id', None)
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                product.delete()
                return Response(data=success, status=200)
            return Response(data=none, status=400)
        return Response(data=value_e, status=400)


class OneProductApi(APIView):

    def get(self, request):
        product_id = request.query_params.get("id", None)
        try:
            product = Product.objects.filter(id=product_id).first()
            serializer = ProductGetSerializer(product, context={"request": request})
            if request.user.is_authenticated:
                view = Views.objects.filter(user=request.user, product=product).first()
                like = Likes.objects.filter(user=request.user, product=product).first()
                if not view:
                    Views.objects.create(user=request.user, product=product)
                views_count = product.views.count()
                likes_count = product.likes.count()
                data = serializer.data
                data['views'] = views_count
                data['likes'] = likes_count
                return Response(data=data, status=200)
            return Response(serializer.data, status=200)
        except:
            return Response(none, status=400)


class ProductAllApi(APIView):
    serializer_class = ProductGetSerializer
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductGetSerializer(products, many=True, context={"request": request})

        return Response(serializer.data, status=200)


class AddLike(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductIdSerializer

    def post(self, request):
        serializer = ProductIdSerializer(data=request.data)
        if serializer.is_valid():
            product = get_product(serializer.validated_data['id'])
            like = Likes.objects.filter(user=request.user, product=product).first()
            if like:
                like.delete()
                return Response(success, 200)
            Likes.objects.create(user=request.user, product=product)
            return Response(success, 200)
        return Response(serializer.errors)




