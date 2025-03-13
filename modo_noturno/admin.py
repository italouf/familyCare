from django.contrib import admin
from .models import ConfiguracaoModoNoturno, HistoricoModoNoturno

@admin.register(ConfiguracaoModoNoturno)
class ConfiguracaoModoNoturnoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'ativo', 'filtro_luz_azul_ativo', 'nao_perturbe_ativo', 'data_atualizacao')
    list_filter = ('ativo', 'filtro_luz_azul_ativo', 'nao_perturbe_ativo')
    search_fields = ('usuario__username',)

@admin.register(HistoricoModoNoturno)
class HistoricoModoNoturnoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_hora_ativacao', 'data_hora_desativacao', 'duracao_minutos', 'ativado_automaticamente')
    list_filter = ('ativado_automaticamente',)
    search_fields = ('usuario__username',)
    date_hierarchy = 'data_hora_ativacao'
