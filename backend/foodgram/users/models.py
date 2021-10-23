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
    is_staff = models.BooleanField(default=False)
