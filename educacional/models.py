from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo para cursos educacionais
class Curso(models.Model):
    """Modelo para armazenar informações sobre cursos disponíveis"""
    CATEGORIA_CHOICES = [
        ('saude', 'Saúde'),
        ('nutricao', 'Nutrição'),
        ('bem_estar', 'Bem-estar'),
        ('tecnologia', 'Tecnologia'),
        ('outro', 'Outro'),
    ]
    
    NIVEL_CHOICES = [
        ('iniciante', 'Iniciante'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
    ]
    
    titulo = models.CharField(max_length=200)  # Título do curso
    descricao = models.TextField()  # Descrição do curso
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)  # Categoria do curso
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='iniciante')  # Nível do curso
    duracao_horas = models.IntegerField(help_text='Duração em horas')  # Duração em horas
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True)  # Imagem do curso
    data_publicacao = models.DateField(default=timezone.now)  # Data de publicação
    gratuito = models.BooleanField(default=False)  # Se o curso é gratuito
    preco = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Preço (se não for gratuito)
    url = models.URLField(blank=True)  # URL do curso
    
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['categoria', 'titulo']
    
    def __str__(self):
        return f'{self.titulo} - {self.get_categoria_display()}'

# Modelo para inscrições em cursos
class InscricaoCurso(models.Model):
    """Modelo para armazenar informações sobre inscrições de usuários em cursos"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inscricoes_cursos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscricoes')
    data_inscricao = models.DateTimeField(default=timezone.now)  # Data da inscrição
    concluido = models.BooleanField(default=False)  # Se o curso foi concluído
    data_conclusao = models.DateTimeField(blank=True, null=True)  # Data de conclusão
    avaliacao = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)  # Avaliação de 1 a 5
    comentario = models.TextField(blank=True)  # Comentário sobre o curso
    
    class Meta:
        verbose_name = 'Inscrição em Curso'
        verbose_name_plural = 'Inscrições em Cursos'
        ordering = ['-data_inscricao']
        unique_together = ['usuario', 'curso']  # Um usuário só pode se inscrever uma vez em cada curso
    
    def __str__(self):
        return f'{self.usuario.username} - {self.curso.titulo}'

# Modelo para e-books
class Ebook(models.Model):
    """Modelo para armazenar informações sobre e-books disponíveis"""
    titulo = models.CharField(max_length=200)  # Título do e-book
    autor = models.CharField(max_length=100)  # Autor do e-book
    descricao = models.TextField()  # Descrição do e-book
    categoria = models.CharField(max_length=50)  # Categoria do e-book
    paginas = models.IntegerField()  # Número de páginas
    capa = models.ImageField(upload_to='ebooks/', blank=True, null=True)  # Capa do e-book
    data_publicacao = models.DateField()  # Data de publicação
    gratuito = models.BooleanField(default=False)  # Se o e-book é gratuito
    preco = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)  # Preço (se não for gratuito)
    arquivo = models.FileField(upload_to='ebooks/arquivos/', blank=True, null=True)  # Arquivo do e-book
    url = models.URLField(blank=True)  # URL para download ou compra
    
    class Meta:
        verbose_name = 'E-book'
        verbose_name_plural = 'E-books'
        ordering = ['categoria', 'titulo']
    
    def __str__(self):
        return f'{self.titulo} - {self.autor}'

# Modelo para videoaulas
class Videoaula(models.Model):
    """Modelo para armazenar informações sobre videoaulas disponíveis"""
    titulo = models.CharField(max_length=200)  # Título da videoaula
    descricao = models.TextField()  # Descrição da videoaula
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='videoaulas', blank=True, null=True)  # Curso relacionado (opcional)
    duracao_minutos = models.IntegerField(help_text='Duração em minutos')  # Duração em minutos
    thumbnail = models.ImageField(upload_to='videoaulas/', blank=True, null=True)  # Thumbnail da videoaula
    url_video = models.URLField()  # URL do vídeo (YouTube, Vimeo, etc)
    data_publicacao = models.DateField(default=timezone.now)  # Data de publicação
    ordem = models.IntegerField(default=0)  # Ordem da videoaula no curso
    
    class Meta:
        verbose_name = 'Videoaula'
        verbose_name_plural = 'Videoaulas'
        ordering = ['curso', 'ordem', 'titulo']
    
    def __str__(self):
        return f'{self.titulo} - {self.duracao_minutos} min'

# Modelo para lista de compras
class ListaCompras(models.Model):
    """Modelo para armazenar listas de compras do usuário"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listas_compras')
    nome = models.CharField(max_length=100)  # Nome da lista
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação
    data_atualizacao = models.DateTimeField(auto_now=True)  # Data de atualização
    concluida = models.BooleanField(default=False)  # Se a lista está concluída
    
    class Meta:
        verbose_name = 'Lista de Compras'
        verbose_name_plural = 'Listas de Compras'
        ordering = ['-data_atualizacao']
    
    def __str__(self):
        return f'Lista de {self.usuario.username}: {self.nome}'

# Modelo para itens da lista de compras
class ItemListaCompras(models.Model):
    """Modelo para armazenar itens de uma lista de compras"""
    lista = models.ForeignKey(ListaCompras, on_delete=models.CASCADE, related_name='itens')
    nome = models.CharField(max_length=100)  # Nome do item
    quantidade = models.IntegerField(default=1)  # Quantidade
    unidade = models.CharField(max_length=20, blank=True)  # Unidade (kg, g, l, etc)
    comprado = models.BooleanField(default=False)  # Se o item foi comprado
    observacao = models.CharField(max_length=200, blank=True)  # Observação sobre o item
    
    class Meta:
        verbose_name = 'Item da Lista de Compras'
        verbose_name_plural = 'Itens da Lista de Compras'
        ordering = ['nome']
    
    def __str__(self):
        return f'{self.nome} ({self.quantidade} {self.unidade})'

# Modelo para agenda de eventos
class Evento(models.Model):
    """Modelo para armazenar eventos na agenda do usuário"""
    TIPO_CHOICES = [
        ('pessoal', 'Pessoal'),
        ('familiar', 'Familiar'),
        ('trabalho', 'Trabalho'),
        ('saude', 'Saúde'),
        ('outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='eventos')
    titulo = models.CharField(max_length=200)  # Título do evento
    descricao = models.TextField(blank=True)  # Descrição do evento
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='pessoal')  # Tipo do evento
    data_inicio = models.DateTimeField()  # Data e hora de início
    data_fim = models.DateTimeField(blank=True, null=True)  # Data e hora de término (opcional)
    local = models.CharField(max_length=200, blank=True)  # Local do evento
    lembrete = models.BooleanField(default=True)  # Se deve enviar lembrete
    tempo_lembrete = models.IntegerField(default=30, help_text='Tempo em minutos')  # Tempo do lembrete antes do evento
    lista_compras = models.ForeignKey('ListaCompras', on_delete=models.SET_NULL, related_name='eventos', blank=True, null=True)  # Lista de compras relacionada
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['data_inicio']
    
    def __str__(self):
        return f'{self.titulo} - {self.get_tipo_display()} - {self.data_inicio.strftime("%d/%m/%Y %H:%M")}'

# Modelo para promoções
class Promocao(models.Model):
    """Modelo para armazenar informações sobre promoções disponíveis"""
    titulo = models.CharField(max_length=200)  # Título da promoção
    descricao = models.TextField()  # Descrição da promoção
    imagem = models.ImageField(upload_to='promocoes/', blank=True, null=True)  # Imagem da promoção
    data_inicio = models.DateField()  # Data de início
    data_fim = models.DateField()  # Data de término
    codigo_cupom = models.CharField(max_length=50, blank=True)  # Código do cupom (se houver)
    url = models.URLField(blank=True)  # URL da promoção
    
    class Meta:
        verbose_name = 'Promoção'
        verbose_name_plural = 'Promoções'
        ordering = ['data_fim', 'titulo']
    
    def __str__(self):
        return f'{self.titulo} (Válido até: {self.data_fim.strftime("%d/%m/%Y")}'

# Modelo para catálogo de filmes/séries
class Midia(models.Model):
    """Modelo para armazenar informações sobre filmes e séries disponíveis"""
    TIPO_CHOICES = [
        ('filme', 'Filme'),
        ('serie', 'Série'),
        ('documentario', 'Documentário'),
    ]
    
    titulo = models.CharField(max_length=200)  # Título da mídia
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)  # Tipo de mídia
    sinopse = models.TextField()  # Sinopse
    ano_lancamento = models.IntegerField()  # Ano de lançamento
    duracao_minutos = models.IntegerField(help_text='Duração em minutos', blank=True, null=True)  # Duração (para filmes)
    temporadas = models.IntegerField(blank=True, null=True)  # Número de temporadas (para séries)
    genero = models.CharField(max_length=100)  # Gênero(s)
    classificacao = models.CharField(max_length=10)  # Classificação indicativa
    poster = models.ImageField(upload_to='midias/', blank=True, null=True)  # Poster da mídia
    url_trailer = models.URLField(blank=True)  # URL do trailer
    disponivel_em = models.CharField(max_length=200, blank=True)  # Onde está disponível (Netflix, Prime, etc)
    
    class Meta:
        verbose_name = 'Mídia'
        verbose_name_plural = 'Mídias'
        ordering = ['-ano_lancamento', 'titulo']
    
    def __str__(self):
        return f'{self.titulo} ({self.ano_lancamento}) - {self.get_tipo_display()}'
