from django.urls import path
from chat.consumers import MyChatConsumer,OnlineGlobal
websocket_urlpatterns=[
    path('ws/ac/<str:room_id>/',MyChatConsumer.as_asgi()),
    path('Global_Online/',OnlineGlobal.as_asgi()),
]