from django.urls import path
from . import views

app_name = 'saude'

urlpatterns = [
    # Atividades Físicas
    path('atividades-fisicas/', views.atividade_fisica_list, name='atividade_fisica_list'),
    path('atividades-fisicas/adicionar/', views.atividade_fisica_create, name='atividade_fisica_create'),
    path('atividades-fisicas/<int:pk>/', views.atividade_fisica_detail, name='atividade_fisica_detail'),
    path('atividades-fisicas/<int:pk>/editar/', views.atividade_fisica_update, name='atividade_fisica_update'),
    path('atividades-fisicas/<int:pk>/excluir/', views.atividade_fisica_delete, name='atividade_fisica_delete'),
    
    # Consumo de Água
    path('consumo-agua/', views.consumo_agua_list, name='consumo_agua_list'),
    path('consumo-agua/adicionar/', views.consumo_agua_create, name='consumo_agua_create'),
    path('consumo-agua/<int:pk>/', views.consumo_agua_detail, name='consumo_agua_detail'),
    path('consumo-agua/<int:pk>/editar/', views.consumo_agua_update, name='consumo_agua_update'),
    path('consumo-agua/<int:pk>/excluir/', views.consumo_agua_delete, name='consumo_agua_delete'),
    
    # Meta de Água
    path('meta-agua/', views.meta_agua_detail, name='meta_agua_detail'),
    path('meta-agua/editar/', views.meta_agua_update, name='meta_agua_update'),
    
    # Monitoramento de Saúde
    path('monitoramento/', views.monitoramento_saude_list, name='monitoramento_saude_list'),
    path('monitoramento/adicionar/', views.monitoramento_saude_create, name='monitoramento_saude_create'),
    path('monitoramento/<int:pk>/', views.monitoramento_saude_detail, name='monitoramento_saude_detail'),
    path('monitoramento/<int:pk>/editar/', views.monitoramento_saude_update, name='monitoramento_saude_update'),
    path('monitoramento/<int:pk>/excluir/', views.monitoramento_saude_delete, name='monitoramento_saude_delete'),
    
    # Dashboard de Saúde
    path('dashboard/', views.saude_dashboard, name='saude_dashboard'),
]