from django.db import models
from django.contrib.auth.models import AbstractUser
import api.constants as const


class UserModel(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(max_length=const.MAX_LENGTH,
                                unique=True, null=False,
                                blank=False, verbose_name="Имя пользователя")
    email = models.EmailField(null=False, blank=False, unique=True,
                              verbose_name="Почта")
    password = models.CharField(max_length=const.MAX_LENGTH,
                                null=False, blank=False, verbose_name="Пароль")
    last_name = models.CharField(max_length=const.MAX_LENGTH,
                                 null=False, blank=False,
                                 verbose_name="Фамилия")
    first_name = models.CharField(max_length=const.MAX_LENGTH,
                                  null=False, blank=False, verbose_name="Имя")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self) -> str:
        return self.username
