from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError

# Importing F for field updates
from django.db.models import F

# Player as the default User
class Player(AbstractUser):
    last_game_player = models.ForeignKey('Game', null=True, blank=True, on_delete=models.SET_NULL, related_name='last_game_player')
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def __str__(self):
        return self.username


# Game model to represent a Tic Tac Toe game
class Game(models.Model):
    EMPTY_BOARD = '---------'
    player_x = models.ForeignKey(Player, related_name='player_x', on_delete=models.CASCADE)
    player_o = models.ForeignKey(Player, related_name='player_o', on_delete=models.CASCADE)
    board = models.CharField(max_length=9, default=EMPTY_BOARD)  # 9 characters for a 3x3 board
    current_turn = models.ForeignKey(Player, related_name='current_turn', on_delete=models.CASCADE)
    last_move_by = models.ForeignKey(Player, related_name='last_move_by', null=True, blank=True, on_delete=models.SET_NULL)
    winner = models.ForeignKey(Player, related_name='winner', null=True, blank=True, on_delete=models.CASCADE)
    is_finished = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.pk}: {self.player_x.username} vs {self.player_o.username}"

    def clean(self):
        if self.player_x == self.player_o:
            raise ValidationError("A player cannot play against themselves.")

    def expire_if_over_24h(self):
        if not self.is_finished and timezone.now() - self.created_at > timedelta(hours=24):
            self.is_finished = True
            if self.last_move_by:
                self.last_move_by.wins = F('wins') + 1
                self.last_move_by.save()
                self.winner = self.last_move_by
                self.current_turn.losses = F('losses') + 1
                self.current_turn.save()
            self.save()
