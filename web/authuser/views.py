from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm, AvatarChangeForm
from friend.models import FriendList, FriendRequest
from django.conf import settings
from .models import User


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.HOME_URL)
    else:
        form = CustomUserCreationForm()

    return render(request, "authuser/register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect(settings.HOME_URL)  # Change 'home' to your desired URL
            else:
                messages.error(request, 'Invalid login credentials.')
    else:
        form = AuthenticationForm()

    return render(request, 'authuser/login.html', {'form': form})


@login_required
def home(request):
    return render(request,
                  "authuser/home.html",
                  {
                      "current_user": request.user.get_short_name(),
                      "friend_list": FriendList.objects.get(user=request.user),
                      "pending_requests_info": FriendRequest().requests_info(request.user),
                      "all_users": request.user.get_all_other_users()})


@login_required
def profile(request, username):
    if username == request.user.username:
        return render(request,
                      "authuser/self-profile.html",
                      {
                          "current_user": request.user.get_short_name(),
                          "info": User.objects.get(username=username).get_profile_page_info(),
                      })
    return render(request,
                  "authuser/profile.html",
                  {
                      "current_user": request.user.get_short_name(),
                      "target_user": username,
                      "info": User.objects.get(username=username).get_profile_page_info(),
                      "name_for_room": request.user.username + ":" + username,
                  })


@login_required
def edit_profile(request):
    if request.method == "POST":
        info_form = CustomUserChangeForm(request.POST, instance=request.user)
        avatar_form = AvatarChangeForm(request.POST, request.FILES, instance=request.user)
        if info_form.is_valid() and avatar_form.is_valid():
            info_form.save()
            avatar_form.save()
            return redirect('authuser:profile', username=request.user.username)
    else:
        info_form = CustomUserChangeForm(instance=request.user)
        avatar_form = AvatarChangeForm(instance=request.user)

    return render(request, "authuser/edit_profile.html", {"form": info_form, "image_form": avatar_form})
