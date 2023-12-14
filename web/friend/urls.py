# urls.py
from django.urls import path
from .views import send_friend_request

app_name = "friend"
urlpatterns = [
    # Other URL patterns
    path('send_friend_request/<str:username>/', send_friend_request, name='send_friend_request'),
]
