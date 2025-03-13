from django.urls import path
from . import views

app_name = 'entretenimento'

urlpatterns = [
    path('', views.MidiaListView.as_view(), name='midia_list'),
    path('midia/<int:pk>/', views.MidiaDetailView.as_view(), name='midia_detail'),
    path('tipo/<str:tipo>/', views.MidiaTipoListView.as_view(), name='midia_tipo'),
    path('categoria/<str:categoria>/', views.MidiaCategoriaListView.as_view(), name='midia_categoria'),
    path('playlist/', views.PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlist/criar/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/<int:pk>/editar/', views.PlaylistUpdateView.as_view(), name='playlist_update'),
    path('playlist/<int:pk>/excluir/', views.PlaylistDeleteView.as_view(), name='playlist_delete'),
    path('playlist/<int:pk>/adicionar-midia/<int:midia_id>/', views.adicionar_midia_playlist, name='adicionar_midia_playlist'),
    path('playlist/<int:pk>/remover-midia/<int:midia_id>/', views.remover_midia_playlist, name='remover_midia_playlist'),
    path('reproduzir/<int:midia_id>/', views.reproduzir_midia, name='reproduzir_midia'),
]