from django.urls import path
from .views import CreateProductApi, ProductAllApi, AddLike

urlpatterns = [
    path('', CreateProductApi.as_view()),
    path('all/', ProductAllApi.as_view()),
    path('product_like/', AddLike.as_view()),
]
