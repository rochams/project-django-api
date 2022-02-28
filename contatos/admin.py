from django.contrib import admin
from .models import Categoria, Contato


class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'sobrenome', 'telefone', 'mostrar')
    list_display_links = ('id', 'nome')
    list_editable = ('telefone', 'mostrar')
    # list_filter = ('id',)


admin.site.register(Categoria)
admin.site.register(Contato, ContatoAdmin)

