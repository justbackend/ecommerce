from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer, ImageSerializer, ProductGetSerializer
success = "Amaliyot muvaffaqiyatli bajarildi"
error = "Xatolik yuz berdi"
none = "Kiritilganlar bo'yicha malumot topilmadi"
value_e = "Malumotlarni to'g'ri shakilda jo'nating"

class CreateProductApi(APIView):
    serializer_class = ProductSerializer
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=201)
        return Response(data=serializer.errors, status=400)

    def get(self, request):
        products = request.user.product.all()
        serializer = ProductGetSerializer(products, many=True)
        return Response(data=serializer.data, status=200)

    def delete(self, request):
        product_id = request.data.get('id', None)
        if product_id:
            product = Product.objects.filter(id=product_id).first()
            if product:
                product.delete()
                return Response(data=success, status=200)
            return Response(data=none, status=400)
        return Response(data=value_e, status=400)


class ProductAllApi(APIView):
    serializer_class = ProductGetSerializer
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductGetSerializer(products, many=True)
        return Response(serializer.data, status=200)



