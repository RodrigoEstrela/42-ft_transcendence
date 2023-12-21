from django.db import models
from django.conf import settings


# Create your models here.
class GameRoom(models.Model):
    name = models.CharField(max_length=255)
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_user1", null=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_user2", null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Game Room"
        verbose_name_plural = "Game Rooms"


class GameHistory(models.Model):
    timestamp = models.DateTimeField(auto_now=True, unique_for_date=True)
    type = models.CharField(max_length=50)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="gamehistory_winner", null=True)
    loser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="gamehistory_user", null=True)
    final_score = models.CharField(max_length=50)
    game_tag = models.CharField(max_length=50, null=True)

    class Meta:
        verbose_name = "Game History"
        verbose_name_plural = "Game History"

    def __str__(self):
        if self.winner and self.loser:
            return f"[{self.timestamp}] [{self.type}] {self.winner} vs {self.loser} -> {self.final_score}"
        elif self.winner:
            return f"[{self.timestamp}] [{self.type}] {self.winner} vs (deleted) -> {self.final_score}"
        elif self.loser:
            return f"[{self.timestamp}] [{self.type}] (deleted) vs {self.loser} -> {self.final_score}"
        else:
            return f"[{self.timestamp}] [{self.type}] (deleted) vs (deleted) -> {self.final_score}"


class GameStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_stats")
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    tournaments_won = models.IntegerField(default=0)
    tournaments_played = models.IntegerField(default=0)
    game_history = models.ManyToManyField(GameHistory, blank=True, related_name="game_stats")

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = "Game Stats"
        verbose_name_plural = "Game Stats"

    def add_win(self):
        self.wins += 1
        self.save()

    def add_loss(self):
        self.losses += 1
        self.save()

    def add_tournament_win(self):
        self.tournaments_won += 1
        self.save()

    def add_tournament_played(self):
        self.tournaments_played += 1
        self.save()

    def add_game_history(self, game_history):
        self.game_history.add(game_history)
        self.save()

    def get_game_stats(self):
        return {
            "wins": self.wins,
            "losses": self.losses,
            "games_played": self.wins + self.losses,
            "tournaments_won": self.tournaments_won,
            "tournaments_played": self.tournaments_played,
        }

    def get_game_history(self):
        return self.game_history.all().order_by("-timestamp")
