from django.urls import path
from . import views

app_name = 'nutricao'

urlpatterns = [
    # Marmitas
    path('marmitas/', views.marmita_list, name='marmita_list'),
    path('marmitas/<int:pk>/', views.marmita_detail, name='marmita_detail'),
    path('marmitas/<int:pk>/avaliar/', views.avaliacao_marmita_create, name='avaliacao_marmita_create'),
    
    # Planos Alimentares
    path('planos-alimentares/', views.plano_alimentar_list, name='plano_alimentar_list'),
    path('planos-alimentares/adicionar/', views.plano_alimentar_create, name='plano_alimentar_create'),
    path('planos-alimentares/<int:pk>/', views.plano_alimentar_detail, name='plano_alimentar_detail'),
    path('planos-alimentares/<int:pk>/editar/', views.plano_alimentar_update, name='plano_alimentar_update'),
    path('planos-alimentares/<int:pk>/excluir/', views.plano_alimentar_delete, name='plano_alimentar_delete'),
    
    # Refeições do Plano Alimentar
    path('planos-alimentares/<int:plano_pk>/refeicoes/adicionar/', views.refeicao_plano_create, name='refeicao_plano_create'),
    path('refeicoes/<int:pk>/editar/', views.refeicao_plano_update, name='refeicao_plano_update'),
    path('refeicoes/<int:pk>/excluir/', views.refeicao_plano_delete, name='refeicao_plano_delete'),
    
    # Dashboard de Nutrição
    path('dashboard/', views.nutricao_dashboard, name='nutricao_dashboard'),
]