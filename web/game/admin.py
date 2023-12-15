from django.contrib import admin
from .models import GameRoom


class GameRoomAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Customize the fields displayed in the list view

    def __str__(self):
        return f"{self.name}"  # Customize the display of each object


admin.site.register(GameRoom, GameRoomAdmin)
