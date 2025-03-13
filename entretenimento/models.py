from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo para mídia de entretenimento
class Midia(models.Model):
    """Modelo para armazenar informações sobre mídias de entretenimento disponíveis"""
    TIPO_CHOICES = [
        ('filme', 'Filme'),
        ('serie', 'Série'),
        ('musica', 'Música'),
        ('jogo', 'Jogo'),
        ('podcast', 'Podcast'),
        ('outro', 'Outro'),
    ]
    
    CATEGORIA_CHOICES = [
        ('acao', 'Ação'),
        ('aventura', 'Aventura'),
        ('comedia', 'Comédia'),
        ('drama', 'Drama'),
        ('ficcao', 'Ficção Científica'),
        ('terror', 'Terror'),
        ('romance', 'Romance'),
        ('documentario', 'Documentário'),
        ('animacao', 'Animação'),
        ('esporte', 'Esporte'),
        ('musical', 'Musical'),
        ('outro', 'Outro'),
    ]
    
    titulo = models.CharField(max_length=200)  # Título da mídia
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)  # Tipo de mídia
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)  # Categoria da mídia
    descricao = models.TextField()  # Descrição da mídia
    ano_lancamento = models.IntegerField()  # Ano de lançamento
    duracao_minutos = models.IntegerField(help_text='Duração em minutos', blank=True, null=True)  # Duração (para filmes, músicas)
    imagem = models.ImageField(upload_to='midias/', blank=True, null=True)  # Imagem da mídia
    link_streaming = models.URLField(blank=True)  # Link para streaming
    artista_autor = models.CharField(max_length=200, blank=True)  # Artista ou autor
    classificacao = models.CharField(max_length=10, blank=True)  # Classificação indicativa
    data_adicao = models.DateTimeField(default=timezone.now)  # Data de adição ao sistema
    
    class Meta:
        verbose_name = 'Mídia'
        verbose_name_plural = 'Mídias'
        ordering = ['-data_adicao', 'titulo']
    
    def __str__(self):
        return f'{self.titulo} - {self.get_tipo_display()} ({self.get_categoria_display()})'

# Modelo para playlists de mídias
class Playlist(models.Model):
    """Modelo para armazenar playlists de mídias criadas pelos usuários"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')  # Usuário que criou a playlist
    nome = models.CharField(max_length=200)  # Nome da playlist
    descricao = models.TextField(blank=True)  # Descrição da playlist
    midias = models.ManyToManyField(Midia, through='ItemPlaylist', related_name='playlists')  # Mídias na playlist
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação
    data_atualizacao = models.DateTimeField(auto_now=True)  # Data de atualização
    publica = models.BooleanField(default=False)  # Se a playlist é pública
    imagem = models.ImageField(upload_to='playlists/', blank=True, null=True)  # Imagem da playlist
    
    class Meta:
        verbose_name = 'Playlist'
        verbose_name_plural = 'Playlists'
        ordering = ['-data_atualizacao']
    
    def __str__(self):
        return f'{self.nome} - {self.usuario.username}'

# Modelo para itens da playlist
class ItemPlaylist(models.Model):
    """Modelo para armazenar itens de uma playlist"""
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='itens')  # Playlist relacionada
    midia = models.ForeignKey(Midia, on_delete=models.CASCADE, related_name='itens_playlist')  # Mídia na playlist
    ordem = models.IntegerField(default=0)  # Ordem na playlist
    data_adicao = models.DateTimeField(auto_now_add=True)  # Data de adição à playlist
    
    class Meta:
        verbose_name = 'Item de Playlist'
        verbose_name_plural = 'Itens de Playlist'
        ordering = ['ordem']
        unique_together = ['playlist', 'midia']  # Uma mídia só pode aparecer uma vez em cada playlist
    
    def __str__(self):
        return f'{self.midia.titulo} - Playlist: {self.playlist.nome}'

# Modelo para histórico de reprodução
class HistoricoReproducao(models.Model):
    """Modelo para armazenar histórico de reprodução de mídias pelos usuários"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_reproducao')  # Usuário que reproduziu
    midia = models.ForeignKey(Midia, on_delete=models.CASCADE, related_name='historico_reproducao')  # Mídia reproduzida
    data_reproducao = models.DateTimeField(default=timezone.now)  # Data e hora da reprodução
    tempo_assistido = models.IntegerField(default=0, help_text='Tempo assistido em segundos')  # Tempo assistido (em segundos)
    concluido = models.BooleanField(default=False)  # Se a reprodução foi concluída
    
    class Meta:
        verbose_name = 'Histórico de Reprodução'
        verbose_name_plural = 'Históricos de Reprodução'
        ordering = ['-data_reproducao']
    
    def __str__(self):
        return f'{self.usuario.username} - {self.midia.titulo} - {self.data_reproducao.strftime("%d/%m/%Y %H:%M")}'
