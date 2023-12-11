from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User
from friend.models import FriendList


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']

        if commit:
            user.save()
            FriendList.objects.create(user=user)
        return user