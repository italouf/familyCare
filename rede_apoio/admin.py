from django.contrib import admin
from .models import ContatoEmergencial, AcionamentoEmergencia, GrupoApoio, ParticipacaoGrupo

@admin.register(ContatoEmergencial)
class ContatoEmergencialAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'tipo', 'telefone', 'prioridade', 'acionamento_rapido')
    list_filter = ('tipo', 'prioridade', 'acionamento_rapido')
    search_fields = ('nome', 'usuario__username', 'telefone')
    list_editable = ('prioridade', 'acionamento_rapido')

@admin.register(AcionamentoEmergencia)
class AcionamentoEmergenciaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contato', 'data_hora', 'atendido')
    list_filter = ('atendido', 'data_hora')
    search_fields = ('usuario__username', 'contato__nome', 'motivo')
    date_hierarchy = 'data_hora'

@admin.register(GrupoApoio)
class GrupoApoioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'local', 'horario')
    list_filter = ('tipo',)
    search_fields = ('nome', 'descricao', 'tipo')

@admin.register(ParticipacaoGrupo)
class ParticipacaoGrupoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'grupo', 'data_entrada', 'ativo')
    list_filter = ('ativo', 'data_entrada')
    search_fields = ('usuario__username', 'grupo__nome')
    date_hierarchy = 'data_entrada'
