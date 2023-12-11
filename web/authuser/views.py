from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from friend.models import FriendList


@login_required
def home(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Get the current user's friend list
        friend_list = FriendList.objects.get(user=request.user)
    else:
        friend_list = None

    return render(request, "authuser/home.html", {"friend_list": friend_list})


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "authuser/register.html", {"form": form})


def login_view(request):

    return HttpResponse("Login view")
