from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatRoom
from authuser.models import User


@login_required
def private_room(request, other_user):
    chats = []
    other_user_obj = User.objects.get(username=other_user)
    if ChatRoom.objects.filter(user1=request.user, user2=other_user_obj).first():
        room_obj = ChatRoom.objects.filter(user1=request.user, user2=other_user_obj).first()
        chats = Chat.objects.filter(room=room_obj).order_by('timestamp')
    elif ChatRoom.objects.filter(user2=request.user, user1=other_user_obj).first():
        room_obj = ChatRoom.objects.filter(user2=request.user, user1=other_user_obj).first()
        chats = Chat.objects.filter(room=room_obj).order_by('timestamp')
    else:
        room_obj = ChatRoom(user1=request.user, user2=other_user_obj, name=f"{request.user.username}_{other_user}")
        room_obj.save()
    return render(request, "chat/room.html", {
        "room_name": room_obj.name,
        "chats": chats,
        "sender": request.user.username,
        "target_user": other_user,
    })
