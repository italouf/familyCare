from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo para catálogo de marmitas
class Marmita(models.Model):
    """Modelo para armazenar informações sobre marmitas disponíveis no catálogo"""
    CATEGORIA_CHOICES = [
        ('fitness', 'Fitness'),
        ('vegetariana', 'Vegetariana'),
        ('geral', 'Geral'),
    ]
    
    REFEICAO_CHOICES = [
        ('cafe_manha', 'Café da Manhã'),
        ('almoco', 'Almoço'),
        ('jantar', 'Jantar'),
        ('sobremesa', 'Sobremesa'),
        ('lanche', 'Lanche'),
    ]
    
    nome = models.CharField(max_length=100)  # Nome da marmita
    descricao = models.TextField()  # Descrição detalhada
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)  # Categoria da marmita
    tipo_refeicao = models.CharField(max_length=20, choices=REFEICAO_CHOICES)  # Tipo de refeição
    calorias = models.IntegerField(help_text='Valor calórico em kcal')  # Valor calórico
    proteinas = models.DecimalField(max_digits=5, decimal_places=2, help_text='Quantidade em gramas')  # Proteínas em g
    carboidratos = models.DecimalField(max_digits=5, decimal_places=2, help_text='Quantidade em gramas')  # Carboidratos em g
    gorduras = models.DecimalField(max_digits=5, decimal_places=2, help_text='Quantidade em gramas')  # Gorduras em g
    preco = models.DecimalField(max_digits=6, decimal_places=2)  # Preço
    imagem = models.ImageField(upload_to='marmitas/', blank=True, null=True)  # Imagem da marmita
    disponivel = models.BooleanField(default=True)  # Se está disponível
    data_cadastro = models.DateTimeField(default=timezone.now)  # Data de cadastro
    
    class Meta:
        verbose_name = 'Marmita'
        verbose_name_plural = 'Marmitas'
        ordering = ['categoria', 'tipo_refeicao', 'nome']
    
    def __str__(self):
        return f'{self.nome} - {self.get_categoria_display()} ({self.get_tipo_refeicao_display()})'

# Modelo para avaliações de marmitas
class AvaliacaoMarmita(models.Model):
    """Modelo para armazenar avaliações de usuários sobre as marmitas"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_marmita')
    marmita = models.ForeignKey(Marmita, on_delete=models.CASCADE, related_name='avaliacoes')
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Nota de 1 a 5
    comentario = models.TextField(blank=True)  # Comentário opcional
    data_avaliacao = models.DateTimeField(default=timezone.now)  # Data da avaliação
    
    class Meta:
        verbose_name = 'Avaliação de Marmita'
        verbose_name_plural = 'Avaliações de Marmitas'
        ordering = ['-data_avaliacao']
        unique_together = ['usuario', 'marmita']  # Um usuário só pode avaliar uma marmita uma vez
    
    def __str__(self):
        return f'Avaliação de {self.usuario.username} para {self.marmita.nome} - Nota: {self.nota}'

# Modelo para plano alimentar do usuário
class PlanoAlimentar(models.Model):
    """Modelo para armazenar o plano alimentar personalizado do usuário"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planos_alimentares')
    data_inicio = models.DateField(default=timezone.now)  # Data de início do plano
    data_fim = models.DateField(blank=True, null=True)  # Data de término (opcional)
    objetivo = models.CharField(max_length=100)  # Objetivo do plano (ex: perda de peso, ganho de massa)
    restricoes = models.TextField(blank=True)  # Restrições alimentares
    observacoes = models.TextField(blank=True)  # Observações adicionais
    ativo = models.BooleanField(default=True)  # Se o plano está ativo
    
    class Meta:
        verbose_name = 'Plano Alimentar'
        verbose_name_plural = 'Planos Alimentares'
        ordering = ['-data_inicio']
    
    def __str__(self):
        return f'Plano Alimentar de {self.usuario.username} - {self.objetivo}'

# Modelo para itens do plano alimentar
class ItemPlanoAlimentar(models.Model):
    """Modelo para armazenar os itens específicos de um plano alimentar"""
    DIA_SEMANA_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    plano = models.ForeignKey(PlanoAlimentar, on_delete=models.CASCADE, related_name='itens')
    marmita = models.ForeignKey(Marmita, on_delete=models.CASCADE, related_name='planos')
    dia_semana = models.IntegerField(choices=DIA_SEMANA_CHOICES)  # Dia da semana
    horario = models.TimeField()  # Horário da refeição
    quantidade = models.IntegerField(default=1)  # Quantidade
    observacao = models.CharField(max_length=200, blank=True)  # Observação específica para este item
    
    class Meta:
        verbose_name = 'Item do Plano Alimentar'
        verbose_name_plural = 'Itens do Plano Alimentar'
        ordering = ['dia_semana', 'horario']
    
    def __str__(self):
        return f'{self.get_dia_semana_display()} - {self.horario.strftime("%H:%M")} - {self.marmita.nome}'
