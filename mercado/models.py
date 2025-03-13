from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo para produtos do mercado online
class Produto(models.Model):
    """Modelo para armazenar informações sobre produtos disponíveis no mercado online"""
    CATEGORIA_CHOICES = [
        ('eletronicos', 'Eletrônicos'),
        ('alimentos', 'Alimentos'),
        ('vestuario', 'Vestuário'),
        ('casa_decoracao', 'Casa e Decoração'),
        ('saude_beleza', 'Saúde e Beleza'),
        ('esportes', 'Esportes e Lazer'),
        ('brinquedos', 'Brinquedos'),
        ('livros', 'Livros'),
        ('outro', 'Outro'),
    ]
    
    nome = models.CharField(max_length=200)  # Nome do produto
    descricao = models.TextField()  # Descrição do produto
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)  # Categoria do produto
    preco = models.DecimalField(max_digits=8, decimal_places=2)  # Preço do produto
    estoque = models.IntegerField(default=0)  # Quantidade em estoque
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)  # Imagem do produto
    data_cadastro = models.DateTimeField(default=timezone.now)  # Data de cadastro
    destaque = models.BooleanField(default=False)  # Se o produto está em destaque
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['categoria', 'nome']
    
    def __str__(self):
        return f'{self.nome} - {self.get_categoria_display()} - R$ {self.preco}'

# Modelo para promoções de produtos
class PromocaoProduto(models.Model):
    """Modelo para armazenar informações sobre promoções de produtos"""
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='promocoes')  # Produto em promoção
    titulo = models.CharField(max_length=200)  # Título da promoção
    descricao = models.TextField(blank=True)  # Descrição da promoção
    desconto = models.DecimalField(max_digits=5, decimal_places=2, help_text='Valor do desconto em porcentagem')  # Desconto em %
    data_inicio = models.DateField()  # Data de início
    data_fim = models.DateField()  # Data de término
    imagem = models.ImageField(upload_to='promocoes_produtos/', blank=True, null=True)  # Imagem da promoção
    codigo_cupom = models.CharField(max_length=50, blank=True)  # Código do cupom (se houver)
    
    class Meta:
        verbose_name = 'Promoção de Produto'
        verbose_name_plural = 'Promoções de Produtos'
        ordering = ['data_fim', 'produto']
    
    def __str__(self):
        return f'{self.titulo} - {self.produto.nome} ({self.desconto}% off)'
    
    @property
    def preco_promocional(self):
        """Calcula o preço promocional do produto"""
        return self.produto.preco * (1 - (self.desconto / 100))
    
    @property
    def esta_ativa(self):
        """Verifica se a promoção está ativa"""
        hoje = timezone.now().date()
        return self.data_inicio <= hoje <= self.data_fim

# Modelo para compra de produtos
class Compra(models.Model):
    """Modelo para armazenar informações sobre compras realizadas pelos usuários"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('cancelada', 'Cancelada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras')  # Usuário que realizou a compra
    lista_compras = models.ForeignKey('educacional.ListaCompras', on_delete=models.SET_NULL, related_name='compras', blank=True, null=True)  # Lista de compras relacionada
    data = models.DateTimeField(default=timezone.now)  # Data da compra
    total = models.DecimalField(max_digits=10, decimal_places=2)  # Valor total da compra
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')  # Status da compra
    observacoes = models.TextField(blank=True)  # Observações adicionais
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-data']
    
    def __str__(self):
        return f'Compra de {self.usuario.username} - {self.data.strftime("%d/%m/%Y %H:%M")} - R$ {self.total}'

# Modelo para itens da compra
class ItemCompra(models.Model):
    """Modelo para armazenar informações sobre itens de uma compra"""
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='itens')  # Compra relacionada
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='itens_compra')  # Produto comprado
    quantidade = models.IntegerField(default=1)  # Quantidade
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)  # Preço unitário no momento da compra
    desconto = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # Desconto aplicado
    
    class Meta:
        verbose_name = 'Item de Compra'
        verbose_name_plural = 'Itens de Compra'
    
    def __str__(self):
        return f'{self.produto.nome} - {self.quantidade} unidade(s)'
    
    @property
    def subtotal(self):
        """Calcula o subtotal do item (preço unitário * quantidade - desconto)"""
        return (self.preco_unitario * self.quantidade) - self.desconto
