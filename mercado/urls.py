from django.urls import path
from . import views

app_name = 'mercado'

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='produto_list'),
    path('produto/<int:pk>/', views.ProdutoDetailView.as_view(), name='produto_detail'),
    path('categoria/<str:categoria>/', views.ProdutoCategoriaListView.as_view(), name='produto_categoria'),
    path('promocoes/', views.PromocaoListView.as_view(), name='promocao_list'),
    path('adicionar-lista/<int:produto_id>/', views.adicionar_produto_lista, name='adicionar_lista'),
    path('remover-lista/<int:produto_id>/', views.remover_produto_lista, name='remover_lista'),
    path('busca/', views.ProdutoBuscaView.as_view(), name='produto_busca'),
]