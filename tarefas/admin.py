from django.contrib import admin
from .models import Tarefa, Lembrete, ServicoBaba

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'usuario', 'prazo', 'status', 'prioridade')
    list_filter = ('status', 'prioridade', 'data_criacao')
    search_fields = ('descricao', 'usuario__username')
    date_hierarchy = 'prazo'

@admin.register(Lembrete)
class LembreteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'data_notificacao', 'tipo', 'lido')
    list_filter = ('tipo', 'lido', 'data_notificacao')
    search_fields = ('titulo', 'descricao', 'usuario__username')
    date_hierarchy = 'data_notificacao'

@admin.register(ServicoBaba)
class ServicoBabaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo_servico', 'data', 'horario_inicio', 'horario_fim', 'status')
    list_filter = ('tipo_servico', 'status', 'data')
    search_fields = ('usuario__username', 'local', 'observacoes')
    date_hierarchy = 'data'