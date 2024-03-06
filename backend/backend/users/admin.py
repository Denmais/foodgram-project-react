from django.contrib import admin
from users.models import UserModel


@admin.register(UserModel)
class UsersAdmin(admin.ModelAdmin):
    pass
