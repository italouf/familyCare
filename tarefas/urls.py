from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    # Tarefas
    path('', views.TarefaListView.as_view(), name='tarefa_list'),
    path('criar/', views.TarefaCreateView.as_view(), name='tarefa_create'),
    path('<int:pk>/editar/', views.TarefaUpdateView.as_view(), name='tarefa_update'),
    path('<int:pk>/excluir/', views.TarefaDeleteView.as_view(), name='tarefa_delete'),
    path('<int:pk>/concluir/', views.tarefa_concluir, name='tarefa_concluir'),
    path('<int:pk>/adicionar-calendario/', views.tarefa_adicionar_calendario, name='tarefa_adicionar_calendario'),
    
    # Calendário
    path('calendario/', views.CalendarioView.as_view(), name='calendario'),
    path('calendario/eventos/', views.calendario_eventos_json, name='calendario_eventos_json'),
    
    # Lembretes
    path('lembretes/', views.LembreteListView.as_view(), name='lembrete_list'),
    path('lembretes/criar/', views.LembreteCreateView.as_view(), name='lembrete_create'),
    path('lembretes/<int:pk>/marcar-lido/', views.lembrete_marcar_lido, name='lembrete_marcar_lido'),
    path('lembretes/nao-lidos/', views.lembretes_nao_lidos, name='lembretes_nao_lidos'),
    
    # Serviço de Babás
    path('babas/', views.ServicoBabaListView.as_view(), name='servico_baba_list'),
    path('babas/criar/', views.ServicoBabaCreateView.as_view(), name='servico_baba_create'),
    path('babas/<int:pk>/', views.ServicoBabaDetailView.as_view(), name='servico_baba_detail'),
    path('babas/<int:pk>/cancelar/', views.servico_baba_cancelar, name='servico_baba_cancelar'),
    path('babas/<int:pk>/contatar/', views.servico_baba_contatar, name='servico_baba_contatar'),
]