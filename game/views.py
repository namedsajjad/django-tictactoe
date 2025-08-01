from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
import random
from django.utils import timezone
from datetime import timedelta
from .models import Player, Game

def index(request):
    return render(request, 'game/index.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not username or not email or not password1 or not password2:
            return render(request, 'auth/register.html', {'error': 'All fields are required.'})
        if password1 != password2:
            return render(request, 'auth/register.html', {'error': 'Passwords do not match.'})
        try:
            Player.objects.get(username=username)
            return render(request, 'auth/register.html', {'error': 'Username already exists.'})
        except Player.DoesNotExist:
            pass
        user = Player.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        return redirect('index')
    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'auth/login.html')
    return render(request, 'auth/login.html')

@login_required
def logout_view(request):
    print("Logging out user:", request.user.username)
    logout(request)
    return redirect('index')

from django.db.models import F
# The F object is a way to refer to model field values directly in queries. It allows you to perform operations on fields without having to retrieve the values first.
def leaderboard(request):
    players = Player.objects.annotate(
        total_games=F('wins') + F('draws') + F('losses')
    ).order_by('-wins', 'draws', 'losses')

    context = {
        'players': players
    }
    return render(request, 'game/leaderboard.html', context)

@login_required
def new_game(request):
    players = Player.objects.filter(last_game_player__isnull=True)
    player_o = random.choice(players)

    game = Game.objects.create(
        player_x=request.user,
        player_o=player_o,
        current_turn=request.user
    )
    request.user.last_game_player = game
    request.user.save()
    player_o.last_game_player = game
    player_o.save()

    return redirect('game', game_id=game.id)

@login_required
def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    ctx = {
        'game_id': game_id,
        'board' : game.board,
        'current_turn': game.current_turn
    }
    return render(request, 'game/game.html', ctx)

@login_required
def move(request, game_id, move_id):
    player = request.user
    game = get_object_or_404(Game, id=game_id)

    if game.last_move_by.username == player.username or game.is_finished:
        return HttpResponseForbidden("Not Today!")


    board_list = list(game.board)

    if player.username == game.player_o.username:
        print(game.player_o.username)
        player == game.player_o.username
        board_list[move_id] = 'O'
        game.last_move_by = request.user
        game.current_turn = game.player_x
    else:
        print(game.player_x.username)
        player == game.player_x.username
        board_list[move_id] = 'X'
        game.last_move_by = request.user
        game.current_turn = game.player_o

    
    game.board = ''.join(board_list)
    game.save()

    print(board_list[move_id])
    pass
