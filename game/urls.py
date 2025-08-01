from django.urls import path, include
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('leaderboard/',leaderboard, name='leaderboard'),
    path('new_game/', new_game, name='new_game'),
    path('game/<int:game_id>', game, name='game'),
    path('move/<int:game_id>/<int:move_id>/', move, name='move'),
]