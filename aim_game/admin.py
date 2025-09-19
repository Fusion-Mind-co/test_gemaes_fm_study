from django.contrib import admin

from .models import GameResult


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ('played_at', 'difficulty', 'score', 'kills', 'accuracy', 'misses')
    list_filter = ('difficulty', 'played_at')
    search_fields = ('difficulty',)
    ordering = ('-played_at',)
