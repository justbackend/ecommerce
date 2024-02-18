from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, Just, ImageSerializer
success = "Amaliyot muvaffaqiyatli bajarildi"
error = "Xatolik yuz berdi"


class CreateProductApi(APIView):
    serializer_class = ProductSerializer
    # parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # images = request.FILES['images']
        # data = request.data
        # data.pop('images')
        # print(request.FILES)
        # print(images)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=success, status=201)
        return Response(data=serializer.errors, status=400)

