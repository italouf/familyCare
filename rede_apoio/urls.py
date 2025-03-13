from django.urls import path
from . import views

app_name = 'rede_apoio'

urlpatterns = [
    # Contatos Emergenciais
    path('contatos-emergenciais/', views.contato_emergencial_list, name='contato_emergencial_list'),
    path('contatos-emergenciais/adicionar/', views.contato_emergencial_create, name='contato_emergencial_create'),
    path('contatos-emergenciais/<int:pk>/', views.contato_emergencial_detail, name='contato_emergencial_detail'),
    path('contatos-emergenciais/<int:pk>/editar/', views.contato_emergencial_update, name='contato_emergencial_update'),
    path('contatos-emergenciais/<int:pk>/excluir/', views.contato_emergencial_delete, name='contato_emergencial_delete'),
    
    # Acionamentos de Emergência
    path('acionamentos/', views.acionamento_emergencia_list, name='acionamento_emergencia_list'),
    path('acionamentos/adicionar/', views.acionamento_emergencia_create, name='acionamento_emergencia_create'),
    path('acionamentos/<int:pk>/', views.acionamento_emergencia_detail, name='acionamento_emergencia_detail'),
    path('acionamentos/<int:pk>/editar/', views.acionamento_emergencia_update, name='acionamento_emergencia_update'),
    path('acionamentos/<int:pk>/excluir/', views.acionamento_emergencia_delete, name='acionamento_emergencia_delete'),
    path('acionamentos/<int:pk>/atender/', views.acionamento_emergencia_atender, name='acionamento_emergencia_atender'),
    
    # Grupos de Apoio
    path('grupos-apoio/', views.grupo_apoio_list, name='grupo_apoio_list'),
    path('grupos-apoio/adicionar/', views.grupo_apoio_create, name='grupo_apoio_create'),
    path('grupos-apoio/<int:pk>/', views.grupo_apoio_detail, name='grupo_apoio_detail'),
    path('grupos-apoio/<int:pk>/editar/', views.grupo_apoio_update, name='grupo_apoio_update'),
    path('grupos-apoio/<int:pk>/participar/', views.grupo_apoio_participar, name='grupo_apoio_participar'),
    
    # Acionamento Rápido
    path('acionamento-rapido/', views.acionamento_rapido, name='acionamento_rapido'),
    
    # Dashboard da Rede de Apoio
    path('dashboard/', views.rede_apoio_dashboard, name='rede_apoio_dashboard'),
]