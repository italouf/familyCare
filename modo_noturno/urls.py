from django.urls import path
from . import views

app_name = 'modo_noturno'

urlpatterns = [
    # Configurações do Modo Noturno
    path('configuracao/', views.configuracao_detail, name='configuracao'),
    path('configuracao/editar/', views.configuracao_update, name='configuracao_update'),
    
    # Ativação/Desativação do Modo Noturno
    path('toggle/', views.modo_noturno_toggle, name='toggle'),
    
    # Histórico de Uso
    path('historico/', views.historico_list, name='historico_list'),
    
    # Configurações Avançadas
    path('configuracao/avancada/', views.configuracao_avancada, name='configuracao_avancada'),
    
    # Estatísticas de Uso
    path('estatisticas/', views.estatisticas, name='estatisticas'),
]