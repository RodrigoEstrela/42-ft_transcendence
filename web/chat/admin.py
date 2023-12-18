from django.contrib import admin
from .models import Chat, ChatRoom


class ChatAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'content')  # Customize the fields displayed in the list view

    def __str__(self):
        return f"{self.user.username} - {self.content}"  # Customize the display of each object


admin.site.register(Chat, ChatAdmin)


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', "user1", "user2", )  # Customize the fields displayed in the list view

    def __str__(self):
        return f"{self.name}"  # Customize the display of each object


admin.site.register(ChatRoom, ChatRoomAdmin)
