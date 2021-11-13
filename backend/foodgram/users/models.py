from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """Model for describing the user."""
    username = models.CharField(
        "Логин",
        max_length=150,
        unique=True,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    password = models.TextField("Пароль", max_length=150)
    email = models.EmailField("Email", max_length=254, unique=True)
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    is_staff = models.BooleanField("Администратор", default=False)

    class Meta:
        ordering = ["id"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Follow(models.Model):
    """Subscription model for recipe author publications."""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Блогер"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"],
                name="unique_pair"
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F("following")),
                name="impossible_subscribe_yourself"
            )
        ]
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
