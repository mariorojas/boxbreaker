from django.contrib import admin

from .models import Attempt, Game


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['pk', 'answer', 'parent_pk', 'parent_answer', 'created_at']

    @admin.display
    def parent_pk(self, obj):
        return obj.parent.pk

    @admin.display
    def parent_answer(self, obj):
        return obj.parent.answer


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = [
        'uuid', 'pk', 'answer', 'owner', 'created_at', 'completed', 'win', 'points'
    ]
