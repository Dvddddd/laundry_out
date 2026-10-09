from django.contrib import admin

from .models import TipoUniforme


@admin.register(TipoUniforme)
class TipoUniformeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'ordem')
    list_filter = ('status',)
    search_fields = ('nome',)
    ordering = ('ordem', 'nome')
