from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

# Modelo para contatos emergenciais
class ContatoEmergencial(models.Model):
    """Modelo para armazenar informações sobre contatos emergenciais do usuário"""
    TIPO_CHOICES = [
        ('familiar', 'Familiar'),
        ('amigo', 'Amigo'),
        ('medico', 'Médico'),
        ('cuidador', 'Cuidador'),
        ('outro', 'Outro'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contatos_emergenciais')
    nome = models.CharField(max_length=100)  # Nome do contato
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)  # Tipo de contato
    telefone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="O número de telefone deve estar no formato: '+999999999'. Até 15 dígitos são permitidos."
    )
    telefone = models.CharField(validators=[telefone_regex], max_length=17)  # Telefone do contato
    email = models.EmailField(blank=True, null=True)  # Email do contato (opcional)
    endereco = models.TextField(blank=True)  # Endereço do contato (opcional)
    observacoes = models.TextField(blank=True)  # Observações adicionais
    prioridade = models.IntegerField(default=5, help_text='Prioridade de 1 a 5 (1 é a mais alta)')  # Prioridade do contato
    acionamento_rapido = models.BooleanField(default=False)  # Se o contato está disponível para acionamento rápido
    
    class Meta:
        verbose_name = 'Contato Emergencial'
        verbose_name_plural = 'Contatos Emergenciais'
        ordering = ['prioridade', 'nome']
    
    def __str__(self):
        return f'{self.nome} - {self.get_tipo_display()} (Prioridade: {self.prioridade})'

# Modelo para registro de acionamentos de emergência
class AcionamentoEmergencia(models.Model):
    """Modelo para armazenar informações sobre acionamentos de emergência realizados pelo usuário"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='acionamentos_emergencia')
    contato = models.ForeignKey(ContatoEmergencial, on_delete=models.CASCADE, related_name='acionamentos')
    data_hora = models.DateTimeField(auto_now_add=True)  # Data e hora do acionamento
    motivo = models.TextField(blank=True)  # Motivo do acionamento (opcional)
    atendido = models.BooleanField(default=False)  # Se o acionamento foi atendido
    observacoes = models.TextField(blank=True)  # Observações adicionais
    
    class Meta:
        verbose_name = 'Acionamento de Emergência'
        verbose_name_plural = 'Acionamentos de Emergência'
        ordering = ['-data_hora']
    
    def __str__(self):
        return f'Acionamento para {self.contato.nome} em {self.data_hora.strftime("%d/%m/%Y %H:%M")}'

# Modelo para grupos de apoio
class GrupoApoio(models.Model):
    """Modelo para armazenar informações sobre grupos de apoio disponíveis"""
    nome = models.CharField(max_length=100)  # Nome do grupo
    descricao = models.TextField()  # Descrição do grupo
    tipo = models.CharField(max_length=50)  # Tipo de grupo (ex: Alzheimer, Parkinson, etc)
    local = models.TextField(blank=True)  # Local de encontro (opcional)
    horario = models.CharField(max_length=100, blank=True)  # Horário de funcionamento (opcional)
    contato = models.CharField(max_length=100, blank=True)  # Contato do grupo (opcional)
    website = models.URLField(blank=True)  # Website do grupo (opcional)
    
    class Meta:
        verbose_name = 'Grupo de Apoio'
        verbose_name_plural = 'Grupos de Apoio'
        ordering = ['nome']
    
    def __str__(self):
        return f'{self.nome} - {self.tipo}'

# Modelo para participação em grupos de apoio
class ParticipacaoGrupo(models.Model):
    """Modelo para armazenar informações sobre participação de usuários em grupos de apoio"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participacoes_grupos')
    grupo = models.ForeignKey(GrupoApoio, on_delete=models.CASCADE, related_name='participantes')
    data_entrada = models.DateTimeField(default=timezone.now)  # Data de entrada no grupo
    ativo = models.BooleanField(default=True)  # Se a participação está ativa
    
    class Meta:
        verbose_name = 'Participação em Grupo'
        verbose_name_plural = 'Participações em Grupos'
        unique_together = ['usuario', 'grupo']  # Um usuário só pode participar uma vez de cada grupo
    
    def __str__(self):
        return f'{self.usuario.username} em {self.grupo.nome}'
