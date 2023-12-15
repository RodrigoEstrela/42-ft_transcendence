from django.urls import path

from . import views

app_name = "game"
urlpatterns = [
    path("1v1/<str:other_user>/", views.private_room, name="private_room"),
]
