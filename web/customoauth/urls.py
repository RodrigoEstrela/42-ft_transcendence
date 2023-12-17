# customoauth/urls.py

from django.urls import path
from .views import YourOAuthView, OAuthCallbackView

urlpatterns = [
    path('login/', YourOAuthView.as_view(), name='oauth-login'),
    path('callback/', OAuthCallbackView.as_view(), name='oauth-callback'),
    # Add other URLs as needed
]
