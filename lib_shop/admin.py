from django.contrib import admin
from .models import Categoria, Livro ,Biblioteca_usuario , saldo_usuario

class LivroAdmin(admin.ModelAdmin):
    filter_horizontal = ('categorias',)  # Adiciona um filtro horizontal para o campo categorias
admin.site.register(Livro,LivroAdmin)
admin.site.register(Categoria)
admin.site.register(Biblioteca_usuario)
admin.site.register(saldo_usuario)
