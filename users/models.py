from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Телефон")
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
