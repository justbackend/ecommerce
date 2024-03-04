from rest_framework import serializers

from ProductsApp.models import Product, ProductImage, Likes


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
        image_query = obj.images.first()
        image = ImageSerializer(image_query)
        return image.data

    class Meta:
        model = Product
        fields = (
            'id', 'user', 'phoneName', 'phoneMarka', 'cost', 'costType', 'phoneMemory', 'phoneColor', 'document',
            'isNew',
            'comment', 'adress', 'phoneNumber', 'time', 'images')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        if request.user.is_authenticated:
            like = Likes.objects.filter(user=request.user, product=instance).first()
            if like:
                representation['liked_status'] = True
                print('i worked')
            else:
                representation['liked_status'] = False
        return representation


class ProductIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()