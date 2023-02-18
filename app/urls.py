from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('like/', LikeImageApi.as_view()),
    path('register/', CreateUserAPI.as_view()),
    path('view-user-image/<str:id>', ViewUserImageApi.as_view()),
    path('view-image/', ViewImageApi.as_view()),
    path('upload-image/', UploadImageApi.as_view()),
]
