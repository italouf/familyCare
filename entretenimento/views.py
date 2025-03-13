from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q

from .models import Midia, Playlist, ItemPlaylist, HistoricoReproducao

# Views para Mídia
class MidiaListView(ListView):
    """View para listar todas as mídias disponíveis"""
    model = Midia
    template_name = 'entretenimento/midia_list.html'
    context_object_name = 'midias'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(titulo__icontains=query) |
                Q(descricao__icontains=query) |
                Q(artista_autor__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = Midia.TIPO_CHOICES
        context['categorias'] = Midia.CATEGORIA_CHOICES
        return context

class MidiaDetailView(DetailView):
    """View para exibir detalhes de uma mídia específica"""
    model = Midia
    template_name = 'entretenimento/midia_detail.html'
    context_object_name = 'midia'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obter mídias relacionadas (mesmo tipo e categoria)
        midia = self.get_object()
        context['midias_relacionadas'] = Midia.objects.filter(
            tipo=midia.tipo, 
            categoria=midia.categoria
        ).exclude(id=midia.id)[:6]
        
        # Verificar se o usuário está logado para mostrar playlists
        if self.request.user.is_authenticated:
            context['playlists'] = Playlist.objects.filter(usuario=self.request.user)
        
        return context

class MidiaTipoListView(ListView):
    """View para listar mídias por tipo (filme, série, música, etc)"""
    model = Midia
    template_name = 'entretenimento/midia_list.html'
    context_object_name = 'midias'
    paginate_by = 12
    
    def get_queryset(self):
        return Midia.objects.filter(tipo=self.kwargs['tipo'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = Midia.TIPO_CHOICES
        context['categorias'] = Midia.CATEGORIA_CHOICES
        context['tipo_atual'] = self.kwargs['tipo']
        context['tipo_display'] = dict(Midia.TIPO_CHOICES).get(self.kwargs['tipo'])
        return context

class MidiaCategoriaListView(ListView):
    """View para listar mídias por categoria (ação, comédia, etc)"""
    model = Midia
    template_name = 'entretenimento/midia_list.html'
    context_object_name = 'midias'
    paginate_by = 12
    
    def get_queryset(self):
        return Midia.objects.filter(categoria=self.kwargs['categoria'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos'] = Midia.TIPO_CHOICES
        context['categorias'] = Midia.CATEGORIA_CHOICES
        context['categoria_atual'] = self.kwargs['categoria']
        context['categoria_display'] = dict(Midia.CATEGORIA_CHOICES).get(self.kwargs['categoria'])
        return context

# Views para Playlist
class PlaylistListView(LoginRequiredMixin, ListView):
    """View para listar playlists do usuário"""
    model = Playlist
    template_name = 'entretenimento/playlist_list.html'
    context_object_name = 'playlists'
    
    def get_queryset(self):
        # Mostrar playlists do usuário e playlists públicas de outros usuários
        return Playlist.objects.filter(
            Q(usuario=self.request.user) | Q(publica=True)
        )

class PlaylistDetailView(DetailView):
    """View para exibir detalhes de uma playlist"""
    model = Playlist
    template_name = 'entretenimento/playlist_detail.html'
    context_object_name = 'playlist'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar se o usuário é o dono da playlist
        context['is_owner'] = self.request.user == self.object.usuario
        return context
    
    def get(self, request, *args, **kwargs):
        playlist = self.get_object()
        # Verificar se o usuário tem permissão para ver a playlist
        if not playlist.publica and request.user != playlist.usuario:
            messages.error(request, 'Você não tem permissão para acessar esta playlist.')
            return redirect('entretenimento:playlist_list')
        return super().get(request, *args, **kwargs)

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    """View para criar uma nova playlist"""
    model = Playlist
    template_name = 'entretenimento/playlist_form.html'
    fields = ['nome', 'descricao', 'publica', 'imagem']
    success_url = reverse_lazy('entretenimento:playlist_list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Playlist criada com sucesso!')
        return super().form_valid(form)

class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar uma playlist existente"""
    model = Playlist
    template_name = 'entretenimento/playlist_form.html'
    fields = ['nome', 'descricao', 'publica', 'imagem']
    
    def get_success_url(self):
        return reverse_lazy('entretenimento:playlist_detail', kwargs={'pk': self.object.pk})
    
    def get(self, request, *args, **kwargs):
        playlist = self.get_object()
        # Verificar se o usuário é o dono da playlist
        if request.user != playlist.usuario:
            messages.error(request, 'Você não tem permissão para editar esta playlist.')
            return redirect('entretenimento:playlist_list')
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Playlist atualizada com sucesso!')
        return super().form_valid(form)

class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    """View para excluir uma playlist"""
    model = Playlist
    template_name = 'entretenimento/playlist_confirm_delete.html'
    success_url = reverse_lazy('entretenimento:playlist_list')
    
    def get(self, request, *args, **kwargs):
        playlist = self.get_object()
        # Verificar se o usuário é o dono da playlist
        if request.user != playlist.usuario:
            messages.error(request, 'Você não tem permissão para excluir esta playlist.')
            return redirect('entretenimento:playlist_list')
        return super().get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Playlist excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Views de função para manipulação de playlists e reprodução
@login_required
def adicionar_midia_playlist(request, pk, midia_id):
    """Adiciona uma mídia a uma playlist"""
    playlist = get_object_or_404(Playlist, pk=pk)
    midia = get_object_or_404(Midia, pk=midia_id)
    
    # Verificar se o usuário é o dono da playlist
    if request.user != playlist.usuario:
        messages.error(request, 'Você não tem permissão para modificar esta playlist.')
        return redirect('entretenimento:midia_detail', pk=midia_id)
    
    # Verificar se a mídia já está na playlist
    if ItemPlaylist.objects.filter(playlist=playlist, midia=midia).exists():
        messages.info(request, f'{midia.titulo} já está na playlist {playlist.nome}.')
    else:
        # Obter a próxima ordem disponível
        ordem = ItemPlaylist.objects.filter(playlist=playlist).count() + 1
        ItemPlaylist.objects.create(playlist=playlist, midia=midia, ordem=ordem)
        messages.success(request, f'{midia.titulo} adicionado à playlist {playlist.nome}.')
    
    # Redirecionar para a página de detalhes da mídia ou da playlist
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('entretenimento:midia_detail', pk=midia_id)

@login_required
def remover_midia_playlist(request, pk, midia_id):
    """Remove uma mídia de uma playlist"""
    playlist = get_object_or_404(Playlist, pk=pk)
    midia = get_object_or_404(Midia, pk=midia_id)
    
    # Verificar se o usuário é o dono da playlist
    if request.user != playlist.usuario:
        messages.error(request, 'Você não tem permissão para modificar esta playlist.')
        return redirect('entretenimento:playlist_detail', pk=pk)
    
    # Remover a mídia da playlist
    item = get_object_or_404(ItemPlaylist, playlist=playlist, midia=midia)
    item.delete()
    
    # Reordenar os itens restantes
    itens = ItemPlaylist.objects.filter(playlist=playlist).order_by('ordem')
    for i, item in enumerate(itens, 1):
        item.ordem = i
        item.save()
    
    messages.success(request, f'{midia.titulo} removido da playlist {playlist.nome}.')
    return redirect('entretenimento:playlist_detail', pk=pk)

@login_required
def reproduzir_midia(request, midia_id):
    """Registra a reprodução de uma mídia pelo usuário"""
    midia = get_object_or_404(Midia, pk=midia_id)
    
    # Registrar no histórico de reprodução
    HistoricoReproducao.objects.create(
        usuario=request.user,
        midia=midia,
        data_reproducao=timezone.now(),
        tempo_assistido=0,  # Inicialmente zero, seria atualizado com JavaScript
        concluido=False
    )
    
    # Redirecionar para o link de streaming da mídia ou para a página de detalhes
    if midia.link_streaming:
        return redirect(midia.link_streaming)
    else:
        messages.info(request, f'Não há link de streaming disponível para {midia.titulo}.')
        return redirect('entretenimento:midia_detail', pk=midia_id)
