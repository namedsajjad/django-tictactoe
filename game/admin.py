from django.contrib import admin
from .models import Player, Game

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_game_player', 'wins', 'draws', 'losses')
    search_fields = ('username',)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_x', 'player_o', 'current_turn', 'winner', 'is_finished', 'created_at', 'board_display')
    search_fields = ('player_x__username', 'player_o__username')
    list_filter = ('is_finished', 'created_at')
    readonly_fields = ('board',)

    def board_display(self, obj):
        return obj.board.replace('-', ' ')
    
    board_display.short_description = 'Board'

    def last_move_player(self, obj):
        return obj.last_move_by.username if obj.last_move_by else 'N/A'
    
    last_move_player.short_description = 'Last Move By'
