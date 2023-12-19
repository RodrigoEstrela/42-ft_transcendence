from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
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
            user.friends_list = FriendList.objects.get(user=user)
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username", "tournament_name", )


class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar",)
