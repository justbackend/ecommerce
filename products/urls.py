from django.urls import path
from .views import CreateProductApi

urlpatterns = [
    path('create/', CreateProductApi.as_view()),
]
