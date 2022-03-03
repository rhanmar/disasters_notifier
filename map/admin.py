from django.contrib import admin
from .models import Point


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'disaster_level',
        'disaster_type',
        'is_verified',
        'created_at',
        'updated_at',
        'created_by',
        'coordinates'
    )
    search_fields = (
        'name',
        'disaster_type',
        'created_by__username',
        'created_by__first_name',
        'created_by__last_name',
    )
