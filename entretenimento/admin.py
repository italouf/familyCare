from django.contrib import admin
from django.utils.html import format_html
from .models import Midia, Playlist, ItemPlaylist, HistoricoReproducao

@admin.register(Midia)
class MidiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'categoria', 'ano_lancamento', 'artista_autor', 'display_imagem')
    list_filter = ('tipo', 'categoria', 'ano_lancamento')
    search_fields = ('titulo', 'descricao', 'artista_autor')
    readonly_fields = ('display_imagem_detail',)
    
    def display_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.imagem.url)
        return "-"
    display_imagem.short_description = 'Imagem'
    
    def display_imagem_detail(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="300" style="max-height: 300px; object-fit: contain;"/>', obj.imagem.url)
        return "-"
    display_imagem_detail.short_description = 'Visualização da Imagem'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'tipo', 'categoria', 'descricao')
        }),
        ('Detalhes', {
            'fields': ('ano_lancamento', 'duracao_minutos', 'artista_autor', 'classificacao')
        }),
        ('Mídia', {
            'fields': ('imagem', 'display_imagem_detail', 'link_streaming')
        })
    )

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'publica', 'data_criacao', 'data_atualizacao')
    list_filter = ('publica', 'data_criacao')
    search_fields = ('nome', 'descricao', 'usuario__username')

@admin.register(ItemPlaylist)
class ItemPlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'midia', 'ordem', 'data_adicao')
    list_filter = ('data_adicao',)
    search_fields = ('playlist__nome', 'midia__titulo')

@admin.register(HistoricoReproducao)
class HistoricoReproducaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'midia', 'data_reproducao', 'tempo_assistido', 'concluido')
    list_filter = ('concluido', 'data_reproducao')
    search_fields = ('usuario__username', 'midia__titulo')
