from django.contrib import admin
from .models import GameRoom, GameHistory


class GameRoomAdmin(admin.ModelAdmin):
    list_display = ('name', "user1", "user2", )  # Customize the fields displayed in the list view

    def __str__(self):
        return f"{self.name}"  # Customize the display of each object


admin.site.register(GameRoom, GameRoomAdmin)


class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'type', 'winner', 'loser', 'final_score', )  # Customize the fields displayed in the list view

    def __str__(self):
        return f"{self.timestamp} - {self.type} - {self.winner} - {self.loser} - {self.final_score}"  # Customize the display of each object


admin.site.register(GameHistory, GameHistoryAdmin)
