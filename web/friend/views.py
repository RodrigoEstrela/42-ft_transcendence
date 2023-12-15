from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FriendRequest
from authuser.models import User
from chat.models import ChatRoom, Chat


@login_required
def send_friend_request(request, username):
    user1 = request.user
    user2 = User.objects.get(username=username)

    # Check if a friend request already exists
    existing_request = (FriendRequest.objects.filter(sender=user1, receiver=user2, is_active=True).first() or
                        FriendRequest.objects.filter(sender=user2, receiver=user1, is_active=True).first())

    if existing_request:
        print(f'A friend request to or from: {user2.username}, is already pending.')
    elif user1.friends_list.is_mutual_friend(user2):
        print(f'You are already friends with {user2.username}.')
    else:
        # Create a new friend request
        friend_request = FriendRequest(sender=user1, receiver=user2)
        friend_request.save()
        messages.success(request, f'Friend request sent to {user2.username}.')

    return redirect('authuser:profile', username=username)


@login_required
def accept_request(request, username):
    user1 = request.user
    user2 = User.objects.get(username=username)

    # Check if a friend request already exists
    friend_request = FriendRequest.objects.filter(sender=user2, receiver=user1, is_active=True).first()

    if friend_request:
        # Accept the friend request
        user1.friends_list.add_friend(user2)
        user2.friends_list.add_friend(user1)
        friend_request.is_active = False
        friend_request.save()
        print(f'You are now friends with {user2.username}.')

    return redirect('authuser:home')


@login_required
def decline_request(request, username):
    user1 = request.user
    user2 = User.objects.get(username=username)

    # Check if a friend request already exists
    friend_request = FriendRequest.objects.filter(sender=user2, receiver=user1, is_active=True).first()

    if friend_request:
        # Reject the friend request
        friend_request.is_active = False
        friend_request.save()
        print(f'You have rejected {user2.username}\'s friend request.')

    return redirect('authuser:home')


@login_required
def cancel_request(request, username):
    user1 = request.user
    user2 = User.objects.get(username=username)

    print(user1, user2)
    # Check if a friend request already exists
    friend_request = FriendRequest.objects.filter(sender=user1, receiver=user2, is_active=True).first()

    if friend_request:
        # Cancel the friend request
        friend_request.is_active = False
        friend_request.save()
        print(f'You have cancelled your friend request to {user2.username}.')

    return redirect('authuser:home')


@login_required
def remove_friend(request, username):
    user1 = request.user
    user2 = User.objects.get(username=username)

    # Check if a friend request already exists
    if user1.friends_list.is_mutual_friend(user2):
        # Remove the friend
        user1.friends_list.remove_friend(user2)
        user2.friends_list.remove_friend(user1)
        print(f'You have removed {user2.username} from your friends list.')
    else:
        print(f'You are not friends with {user2.username}.')

    return redirect('authuser:home')
