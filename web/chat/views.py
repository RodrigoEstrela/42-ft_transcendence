from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat, ChatRoom


@login_required
def index(request):
    return render(request, 'chat/index.html')


@login_required
def room(request, room_name):
    room = ChatRoom.objects.filter(name=room_name).first()
    chats = []
    if room:
        chats = Chat.objects.filter(room=room)
    else:
        room = ChatRoom(name=room_name)
        room.save()

    return render(request, "chat/room.html", {"room_name": room_name, "chats": chats, "sender": request.user.username})
