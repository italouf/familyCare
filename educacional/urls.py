from django.urls import path
from . import views

app_name = 'educacional'

urlpatterns = [
    # Cursos
    path('cursos/', views.curso_list, name='curso_list'),
    path('cursos/<int:pk>/', views.curso_detail, name='curso_detail'),
    path('cursos/<int:pk>/inscrever/', views.curso_inscrever, name='curso_inscrever'),
    
    # E-books
    path('ebooks/', views.ebook_list, name='ebook_list'),
    path('ebooks/<int:pk>/', views.ebook_detail, name='ebook_detail'),
    path('ebooks/<int:pk>/download/', views.ebook_download, name='ebook_download'),
    
    # Videoaulas
    path('videoaulas/', views.videoaula_list, name='videoaula_list'),
    path('videoaulas/<int:pk>/', views.videoaula_detail, name='videoaula_detail'),
    path('videoaulas/<int:pk>/assistir/', views.videoaula_assistir, name='videoaula_assistir'),
    
    # Catálogo de Mídias
    path('midias/', views.midia_list, name='midia_list'),
    path('midias/<int:pk>/', views.midia_detail, name='midia_detail'),
    
    # Progresso Educacional
    path('progresso/', views.progresso_educacional, name='progresso_educacional'),
    
    # Dashboard Educacional
    path('dashboard/', views.educacional_dashboard, name='educacional_dashboard'),
    
    # Lista de Compras
    path('lista-compras/', views.lista_compras_list, name='lista_compras_list'),
    path('lista-compras/nova/', views.lista_compras_create, name='lista_compras_create'),
    path('lista-compras/<int:pk>/', views.lista_compras_detail, name='lista_compras_detail'),
    path('lista-compras/<int:pk>/editar/', views.lista_compras_edit, name='lista_compras_edit'),
    path('lista-compras/<int:pk>/excluir/', views.lista_compras_delete, name='lista_compras_delete'),
    
    # Eventos
    path('eventos/', views.evento_list, name='evento_list'),
    path('eventos/<int:pk>/', views.evento_detail, name='evento_detail'),
    path('eventos/<int:pk>/participar/', views.evento_participar, name='evento_participar'),
    path('eventos/<int:pk>/cancelar/', views.evento_cancelar, name='evento_cancelar'),
]