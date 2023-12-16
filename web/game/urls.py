from django.urls import path

from . import views

app_name = "game"
urlpatterns = [
    path("1v1/<str:other_user>/", views.remote_room, name="remote_room"),
    path("local/", views.local_room, name="local_room"),
]
