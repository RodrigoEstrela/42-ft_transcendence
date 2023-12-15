from django.urls import path

from . import views

app_name = "chat"
urlpatterns = [
    # path("", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),
    path("dm/<str:other_user>/", views.private_room, name="private_room"),
]
