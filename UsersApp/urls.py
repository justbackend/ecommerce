from django.urls import path
from .views import RegisterApi, LikeAddApi, UserApi, BucketAddApi
urlpatterns = [
    path('', UserApi.as_view(), name='user'),
    path('register/', RegisterApi.as_view(), name='register'),
    path('liked/', LikeAddApi.as_view(), name='toLiked'),
    path('bucket/', BucketAddApi.as_view(), name='bucket'),
]
