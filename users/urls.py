from django.urls import path
from .views import RegisterApi, ProfileEditApi, LikeAddApi
urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('update/', ProfileEditApi.as_view(), name='update_user'),
    path('toLiked/', LikeAddApi.as_view(), name='toLiked' )

]