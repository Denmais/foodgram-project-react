from django.contrib import admin
from users.models import UserModel
from django.contrib.auth.admin import UserAdmin


@admin.register(UserModel)
class UsersAdmin(UserAdmin):
    list_display = ('pk', 'username', 'email', 'first_name', 'last_name',
                    'password')
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')
    list_display_links = ('pk', 'username', 'email', 'first_name', 'last_name',
                          'password')
