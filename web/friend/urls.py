# urls.py
from django.urls import path
from .views import *

app_name = "friend"
urlpatterns = [
    path('send_friend_request/<str:username>/', send_friend_request, name='send_friend_request'),
    path('accept_request/<str:username>/', accept_request, name='accept_request'),
    path('decline_request/<str:username>/', decline_request, name='decline_request'),
    path('cancel_request/<str:username>/', cancel_request, name='cancel_request'),
    path('remove_friend/<str:username>/', remove_friend, name='remove_friend'),
]
