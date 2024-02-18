from rest_framework import serializers

from products.models import Product, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = Product
        fields = ('user', 'phoneName', 'phoneMarka', 'cost', 'costType', 'phoneMemory', 'phoneColor', 'document', 'isNew', 'comment', 'adress', 'phoneNumber', 'time', 'images')

    def save(self, **kwargs):
        images = self.validated_data.pop('images')
        product = Product.objects.create(**self.validated_data)
        print(product.id,"//////////////////////////////////////////////////")
        for image in images:

            print(image, "///////////////////////////////////////////////////////")
            ProductImage.objects.create(product=product, image=image)
        return product

class Just(serializers.Serializer):
    img = serializers.FileField()


