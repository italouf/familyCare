from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo para controle de atividade física
class AtividadeFisica(models.Model):
    """Modelo para armazenar informações sobre atividades físicas realizadas pelo usuário"""
    TIPO_CHOICES = [
        ('musculacao', 'Musculação'),
        ('natacao', 'Natação'),
        ('caminhada', 'Caminhada'),
        ('artes_marciais', 'Artes Marciais'),
        ('outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atividades_fisicas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    data = models.DateField(default=timezone.now)
    duracao = models.IntegerField(help_text='Duração em minutos')  # Duração em minutos
    calorias_gastas = models.IntegerField(blank=True, null=True)  # Calorias gastas (opcional)
    descricao = models.TextField(blank=True)  # Descrição da atividade (opcional)
    
    class Meta:
        verbose_name = 'Atividade Física'
        verbose_name_plural = 'Atividades Físicas'
        ordering = ['-data']
    
    def __str__(self):
        return f'{self.get_tipo_display()} - {self.data}'

# Modelo para acompanhamento de metas diárias de água
class ConsumoAgua(models.Model):
    """Modelo para armazenar informações sobre o consumo diário de água"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consumos_agua')
    data = models.DateField(default=timezone.now)
    quantidade_ml = models.IntegerField(help_text='Quantidade em mililitros')  # Quantidade em ml
    horario = models.TimeField(default=timezone.now)  # Horário do consumo
    observacoes = models.TextField(blank=True, null=True)  # Campo para observações opcionais
    
    class Meta:
        verbose_name = 'Consumo de Água'
        verbose_name_plural = 'Consumos de Água'
        ordering = ['-data', '-horario']
    
    def __str__(self):
        return f'{self.usuario.username} - {self.data} - {self.quantidade_ml}ml'

# Modelo para meta diária de água
class MetaAgua(models.Model):
    """Modelo para armazenar a meta diária de consumo de água do usuário"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='meta_agua')
    quantidade_diaria_ml = models.IntegerField(default=2000, help_text='Meta diária em mililitros')  # Meta diária em ml
    lembrete_ativo = models.BooleanField(default=True)  # Se o lembrete está ativo
    intervalo_lembretes = models.IntegerField(default=60, help_text='Intervalo em minutos')  # Intervalo em minutos
    
    class Meta:
        verbose_name = 'Meta de Água'
        verbose_name_plural = 'Metas de Água'
    
    def __str__(self):
        return f'Meta de {self.usuario.username}: {self.quantidade_diaria_ml}ml'

# Modelo para monitoramento de saúde
class MonitoramentoSaude(models.Model):
    """Modelo para armazenar informações sobre o monitoramento diário de saúde"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='monitoramentos_saude')
    data = models.DateField(default=timezone.now)
    passos = models.IntegerField(blank=True, null=True)  # Número de passos
    horas_sono = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)  # Horas de sono
    calorias_gastas = models.IntegerField(blank=True, null=True)  # Calorias gastas
    frequencia_cardiaca_media = models.IntegerField(blank=True, null=True)  # Frequência cardíaca média
    frequencia_cardiaca_repouso = models.IntegerField(blank=True, null=True)  # Frequência cardíaca em repouso
    observacoes = models.TextField(blank=True)  # Observações adicionais
    
    class Meta:
        verbose_name = 'Monitoramento de Saúde'
        verbose_name_plural = 'Monitoramentos de Saúde'
        ordering = ['-data']
    
    def __str__(self):
        return f'Monitoramento de {self.usuario.username} - {self.data}'
