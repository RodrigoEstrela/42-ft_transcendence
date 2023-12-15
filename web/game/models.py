from django.db import models
from django.conf import settings


# Create your models here.
class GameRoom(models.Model):
    name = models.CharField(max_length=255)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_user1", null=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_user2", null=True)

    def __str__(self):
        return f"{self.name}"
