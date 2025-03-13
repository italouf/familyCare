from django.contrib import admin
from .models import Marmita, AvaliacaoMarmita, PlanoAlimentar, ItemPlanoAlimentar

@admin.register(Marmita)
class MarmitaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'tipo_refeicao', 'calorias', 'preco', 'disponivel')
    list_filter = ('categoria', 'tipo_refeicao', 'disponivel')
    search_fields = ('nome', 'descricao')
    list_editable = ('disponivel', 'preco')

@admin.register(AvaliacaoMarmita)
class AvaliacaoMarmitaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'marmita', 'nota', 'data_avaliacao')
    list_filter = ('nota', 'data_avaliacao')
    search_fields = ('usuario__username', 'marmita__nome', 'comentario')
    date_hierarchy = 'data_avaliacao'

@admin.register(PlanoAlimentar)
class PlanoAlimentarAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'objetivo', 'data_inicio', 'data_fim', 'ativo')
    list_filter = ('ativo', 'data_inicio')
    search_fields = ('usuario__username', 'objetivo', 'restricoes')
    date_hierarchy = 'data_inicio'

@admin.register(ItemPlanoAlimentar)
class ItemPlanoAlimentarAdmin(admin.ModelAdmin):
    list_display = ('plano', 'marmita', 'dia_semana', 'horario', 'quantidade')
    list_filter = ('dia_semana',)
    search_fields = ('plano__usuario__username', 'marmita__nome', 'observacao')
