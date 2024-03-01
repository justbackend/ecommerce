from rest_framework import serializers

from ProductsApp.models import Product, ProductImage


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'phoneName', 'phoneMarka', 'cost', 'costType', 'phoneMemory', 'phoneColor', 'document', 'isNew',
            'comment', 'adress', 'phoneNumber', 'time', 'images')

    def save(self, **kwargs):
        images = self.validated_data.pop('images')
        product = Product.objects.create(user=self.context['request'].user, **self.validated_data)
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product
    # def update(self, instance, validated_data):


class ProductGetSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    def get_images(self, obj):
        image_query = obj.images.all()
        image = ImageSerializer(image_query, many=True)
        return image.data

    class Meta:
        model = Product
        fields = (
            'id', 'user', 'phoneName', 'phoneMarka', 'cost', 'costType', 'phoneMemory', 'phoneColor', 'document',
            'isNew',
            'comment', 'adress', 'phoneNumber', 'time', 'images')


class ProductIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()