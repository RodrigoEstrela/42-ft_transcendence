from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import GameRoom
from authuser.models import User


@login_required
def remote_room(request, other_user):
    other_user_obj = User.objects.get(username=other_user)
    if GameRoom.objects.filter(user1=request.user, user2=other_user_obj).first():
        room_obj = GameRoom.objects.filter(user1=request.user, user2=other_user_obj).first()
    elif GameRoom.objects.filter(user2=request.user, user1=other_user_obj).first():
        room_obj = GameRoom.objects.filter(user2=request.user, user1=other_user_obj).first()
    else:
        room_obj = GameRoom(user1=request.user, user2=other_user_obj, name=f"{request.user.username}_{other_user}")
        room_obj.save()
    return render(request, "game/game.html", {
        "room_name": room_obj.name,
        "sender": request.user.username})


@login_required
def local_room(request):
    return render(request, "game/game.html", {
        "room_name": request.user.username,
    })
