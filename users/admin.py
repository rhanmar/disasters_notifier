from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'unique_code')
    readonly_fields = ('unique_code',)


admin.site.register(User, UserAdmin)
