from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):

    username = models.CharField(max_length=100, unique=True, null=False,
                                blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    first_name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)
