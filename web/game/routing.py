# game/routing.py
from django.urls import re_path

from . import consumers

game_websocket_urlpatterns = [
    re_path(r"ws/game/(?P<room_name>\w+)/$", consumers.GameConsumer.as_asgi())
]
