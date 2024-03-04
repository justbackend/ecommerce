from django.urls import path
from .views import ProductApi, ProductAllApi, AddLike, OneProductApi, ImageApi, ProductFilterApi

urlpatterns = [
    path('', ProductApi.as_view()),
    path('all/', ProductAllApi.as_view()),
    path('product_like/', AddLike.as_view()),
    path('one_product/', OneProductApi.as_view()),
    path('image/', ImageApi.as_view()),
    path('search/', ProductFilterApi.as_view()),
]
