# customoauth/views.py
import os

from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import login
import requests
from authuser.models import User
from django.http import HttpResponseBadRequest
from friend.models import FriendList
from django.contrib.auth import get_user_model


class YourOAuthView(View):
    def get(self, request, *args, **kwargs):
        # Redirect users to the OAuth provider's authorization URL
        authorization_url = "https://api.intra.42.fr/oauth/authorize?client_id=u-s4t2ud-f81ae818459e61942c018dc4a81daa38227753acade2e384dfce29a493bb76ba&redirect_uri=http%3A%2F%2F0.0.0.0%3A8000%2Foauth%2Fcallback&response_type=code"
        return redirect(authorization_url)


class OAuthCallbackView(View):
    def get(self, request, *args, **kwargs):
        # Retrieve the authorization code from the query parameters
        code = request.GET.get('code')

        if code:
            # Exchange the authorization code for an access token
            access_token = self.exchange_code_for_access_token(code)

            # Fetch user information using the access token
            user_info = self.get_user_info(access_token)

            # Log in the user
            user = self.get_or_create_user(user_info)
            login(request, user)

            # Redirect to a success page or the home page
            return redirect('authuser:home')  # Replace 'home' with your home page URL

        # Handle the case where the authorization code is not present or there was an error
        return HttpResponseBadRequest("Invalid authorization code or OAuth2 error")

    def exchange_code_for_access_token(self, code):
        # Customize this method based on your OAuth2 provider's specifications
        token_url = "https://api.intra.42.fr/oauth/token"
        client_id = "u-s4t2ud-f81ae818459e61942c018dc4a81daa38227753acade2e384dfce29a493bb76ba"
        client_secret = "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"
        redirect_uri = "http://0.0.0.0:8000/oauth/callback"

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
        }

        response = requests.post(token_url, data=data)
        response_data = response.json()

        if response_data['access_token']:
            return response_data['access_token']
        else:
            # Handle the case where the token exchange failed
            return None

    def get_user_info(self, access_token):
        # Customize this method based on your OAuth2 provider's specifications
        user_info_url = "https://api.intra.42.fr/v2/me"
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.get(user_info_url, headers=headers)
        info = {
            'username': response.json()['login'],
            'email': response.json()['email'],
        }
        return info

    def get_or_create_user(self, user_info):
        User = get_user_model()
        # check if user exists
        try:
            user = User.objects.get(username=user_info['username'], email=user_info['email'])

        except User.DoesNotExist:
            # Create a new user
            user = User.objects.create_user(email=user_info['email'], username=user_info['username'])

            # Assuming you want to set is_active to True for new users
            user.is_active = True
            user.save()

            FriendList.objects.create(user=user)
            user.friends_list = FriendList.objects.get(user=user)
            user.save()

        return user
