from django.urls import path
from .views import CreateProductApi, ProductAllApi

urlpatterns = [
    path('', CreateProductApi.as_view()),
    path('all/', ProductAllApi.as_view()),
]
