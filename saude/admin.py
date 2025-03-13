from django.contrib import admin
from .models import AtividadeFisica, ConsumoAgua, MetaAgua, MonitoramentoSaude

@admin.register(AtividadeFisica)
class AtividadeFisicaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'data', 'duracao', 'calorias_gastas')
    list_filter = ('tipo', 'data')
    search_fields = ('usuario__username', 'descricao')
    date_hierarchy = 'data'

@admin.register(ConsumoAgua)
class ConsumoAguaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'quantidade_ml', 'horario')
    list_filter = ('data',)
    search_fields = ('usuario__username', 'observacoes')
    date_hierarchy = 'data'

@admin.register(MetaAgua)
class MetaAguaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'quantidade_diaria_ml', 'lembrete_ativo', 'intervalo_lembretes')
    list_filter = ('lembrete_ativo',)
    search_fields = ('usuario__username',)

@admin.register(MonitoramentoSaude)
class MonitoramentoSaudeAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'passos', 'horas_sono', 'calorias_gastas')
    list_filter = ('data',)
    search_fields = ('usuario__username', 'observacoes')
    date_hierarchy = 'data'
