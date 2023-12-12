from django.db import models
from django.conf import settings


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey("ChatRoom", on_delete=models.CASCADE)
    username = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.room} - {self.user.username} - {self.content}"


class ChatRoom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
