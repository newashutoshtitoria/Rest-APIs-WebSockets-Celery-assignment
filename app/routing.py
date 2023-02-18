from django.urls import path
from .consumers import *

websocket_urlpatterns =[
    path('ws/notify/<str:group_name>', MyNotifications.as_asgi()),
]