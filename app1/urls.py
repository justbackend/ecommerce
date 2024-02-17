from django.urls import path
from . import views
urlpatterns = [
    path('', views.RegisterApi.as_view(), name='index')
]