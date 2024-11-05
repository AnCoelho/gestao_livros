from django.contrib import admin
from .models import Autor, Livro

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    search_fields = ['nome']

@admin.register(Livro)
class LivroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'autor', 'data_publicacao', 'numero_paginas')
    search_fields = ['titulo']
    list_filter = ['autor', 'data_publicacao']

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)