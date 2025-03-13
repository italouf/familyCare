from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from educacional.models import Evento

# Modelo para tarefas diárias
class Tarefa(models.Model):
    """Modelo para armazenar informações sobre tarefas diárias do usuário"""
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluida', 'Concluída'),
    ]
    
    PRIORIDADE_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Média'),
        ('baixa', 'Baixa'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tarefas')
    descricao = models.CharField(max_length=200)  # Descrição da tarefa
    prazo = models.DateTimeField()  # Prazo para conclusão
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pendente')  # Status da tarefa
    prioridade = models.CharField(max_length=5, choices=PRIORIDADE_CHOICES, default='media')  # Prioridade da tarefa
    data_criacao = models.DateTimeField(auto_now_add=True)  # Data de criação
    data_conclusao = models.DateTimeField(blank=True, null=True)  # Data de conclusão
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, related_name='tarefas', blank=True, null=True)  # Evento relacionado
    
    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['prazo', 'prioridade']
    
    def __str__(self):
        return f'{self.descricao} - {self.get_prioridade_display()} - {self.prazo.strftime("%d/%m/%Y %H:%M")}'
    
    def concluir(self):
        """Marca a tarefa como concluída e registra a data de conclusão"""
        self.status = 'concluida'
        self.data_conclusao = timezone.now()
        self.save()

# Modelo para lembretes prioritários
class Lembrete(models.Model):
    """Modelo para armazenar lembretes prioritários do usuário"""
    TIPO_CHOICES = [
        ('importante', 'Importante'),
        ('urgente', 'Urgente'),
        ('informativo', 'Informativo'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lembretes')
    titulo = models.CharField(max_length=100)  # Título do lembrete
    descricao = models.TextField()  # Descrição do lembrete
    data_notificacao = models.DateTimeField()  # Data e hora da notificação
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default='informativo')  # Tipo do lembrete
    lido = models.BooleanField(default=False)  # Se o lembrete foi lido
    tarefa = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name='lembretes', blank=True, null=True)  # Tarefa relacionada
    
    class Meta:
        verbose_name = 'Lembrete'
        verbose_name_plural = 'Lembretes'
        ordering = ['-data_notificacao']
    
    def __str__(self):
        return f'{self.titulo} - {self.get_tipo_display()} - {self.data_notificacao.strftime("%d/%m/%Y %H:%M")}'
    
    def marcar_como_lido(self):
        """Marca o lembrete como lido"""
        self.lido = True
        self.save()

# Modelo para serviço de babás
class ServicoBaba(models.Model):
    """Modelo para armazenar informações sobre serviços de babá solicitados pelo usuário"""
    TIPO_SERVICO_CHOICES = [
        ('eventual', 'Eventual'),
        ('fixo', 'Fixo'),
        ('personalizado', 'Personalizado'),
    ]
    
    STATUS_CHOICES = [
        ('agendado', 'Agendado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='servicos_baba')
    tipo_servico = models.CharField(max_length=15, choices=TIPO_SERVICO_CHOICES)  # Tipo de serviço
    data = models.DateField()  # Data do serviço
    horario_inicio = models.TimeField()  # Horário de início
    horario_fim = models.TimeField()  # Horário de término
    local = models.CharField(max_length=200)  # Local do serviço
    observacoes = models.TextField(blank=True)  # Observações adicionais
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='agendado')  # Status do serviço
    contato = models.ForeignKey('rede_apoio.ContatoEmergencial', on_delete=models.SET_NULL, blank=True, null=True, related_name='servicos_baba')  # Contato da babá
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL, blank=True, null=True, related_name='servicos_baba')  # Evento relacionado
    
    class Meta:
        verbose_name = 'Serviço de Babá'
        verbose_name_plural = 'Serviços de Babá'
        ordering = ['-data', 'horario_inicio']
    
    def __str__(self):
        return f'Serviço de Babá - {self.get_tipo_servico_display()} - {self.data.strftime("%d/%m/%Y")}'
    
    def cancelar(self):
        """Cancela o serviço de babá"""
        self.status = 'cancelado'
        self.save()
        
        # Se houver um evento associado, excluí-lo
        if self.evento:
            self.evento.delete()
            self.evento = None
            self.save()