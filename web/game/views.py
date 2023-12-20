from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GameRoom, GameHistory
from authuser.models import User
import secrets
import string
from django.shortcuts import get_object_or_404
from datetime import datetime


def generate_random_string(length):
    characters = string.ascii_letters + string.digits + "_"
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


@login_required
def remote_room(request, other_user):
    other_user_obj = User.objects.get(username=other_user)
    if GameRoom.objects.filter(user1=request.user, user2=other_user_obj).first():
        room_obj = GameRoom.objects.filter(user1=request.user, user2=other_user_obj).first()
    elif GameRoom.objects.filter(user2=request.user, user1=other_user_obj).first():
        room_obj = GameRoom.objects.filter(user2=request.user, user1=other_user_obj).first()
    else:
        room_obj = GameRoom(user1=request.user, user2=other_user_obj, name=generate_random_string(9))
        room_obj.save()
    return render(request, "game/game.html", {
        "room_name": room_obj.name,
        "sender": request.user.id,
        "user1": room_obj.user1.id,
        "user2": room_obj.user2.id,
        "player0": room_obj.user1.username,
        "player1": room_obj.user2.username,
    })


@login_required
def local_room(request):
    return render(request, "game/game.html", {
        "room_name": generate_random_string(9),
    })


@login_required
def game_ending(request):
    # Get parameters from request
    game_info = request.GET.get('gameinfo', None)
    game_tag = request.GET.get('gametag', None)
    room_name = request.GET.get('roomname', None)
    # Parse game_info string from request
    users = game_info.split('|')
    winner_id = users[0].split(':')[0]
    winner_score = users[0].split(':')[1]
    loser_id = users[1].split(':')[0]
    loser_score = users[1].split(':')[1]
    # Get User objects
    winner = get_object_or_404(User, id=winner_id)
    loser = get_object_or_404(User, id=loser_id)
    # Set up variables to populate entry in GameHistory table
    final_score = f"{winner_score}:{loser_score}"
    # Check if the entry already exists
    existing_entry = GameHistory.objects.filter(game_tag=game_tag).first()
    if not existing_entry:
        # Entry does not exist, create a new one
        game_history = GameHistory(type="1v1", winner=winner, loser=loser, final_score=final_score, game_tag=game_tag)
        game_history.save()
    # Return to game room
    room_obj = GameRoom.objects.filter(name=room_name).first()
    other_user = room_obj.user1.username if room_obj.user1.username != request.user.username else room_obj.user2.username
    return redirect('game:remote_room', other_user=other_user)
