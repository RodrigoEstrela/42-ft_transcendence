from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendRequest
from authuser.models import User


@login_required
def send_friend_request(request, username):
    sender = request.user
    receiver = User.objects.get(username=username)

    # Check if a friend request already exists
    existing_request = FriendRequest.objects.filter(sender=sender, receiver=receiver, is_active=True).first()

    if existing_request:
        messages.warning(request, f'A friend request to {receiver.username} is already pending.')
    else:
        # Create a new friend request
        friend_request = FriendRequest(sender=sender, receiver=receiver)
        friend_request.save()
        messages.success(request, f'Friend request sent to {receiver.username}.')

    return redirect('authuser:profile', username=username)
