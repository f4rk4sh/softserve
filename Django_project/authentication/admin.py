from django.contrib import admin
from authentication.models import Regular, Moderator


@admin.register(Regular)
class RegularAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ['user']
