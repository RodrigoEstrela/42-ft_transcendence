from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models
from django.utils import timezone
from friend.models import FriendList
from game.models import GameStats


class CustomUserManager(UserManager):
    def __create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_staff", False)

        return self.__create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.__create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    tournament_name = models.CharField(max_length=255, blank=True, default="")
    avatar = models.ImageField(null=True, blank=True, upload_to="avatars/", default="avatars/default_avatar.jpg")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    friends_list = models.OneToOneField(FriendList, on_delete=models.CASCADE, null=True, blank=True, related_name="user_friend_list")
    game_stats = models.OneToOneField(GameStats, on_delete=models.CASCADE, null=True, blank=True, related_name="user_game_stats")

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.username

    def get_profile_page_info(self):
        return {
            "avatar": self.avatar if self.avatar else "/media/avatars/default_avatar.jpg",
            "username": self.username,
            "email": self.email,
            "tournament_name": self.tournament_name,
            "date_joined": self.date_joined,
            "last_login": self.last_login,
            "status": self.is_active,
        }

    def get_all_other_users(self):
        return User.objects.filter(is_staff=False).exclude(username=self.username)
