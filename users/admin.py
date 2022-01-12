from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'telegram_id', 'auth_token')


admin.site.register(User, UserAdmin)
