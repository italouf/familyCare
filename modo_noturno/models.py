from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Modelo para configurações do modo noturno
class ConfiguracaoModoNoturno(models.Model):
    """Modelo para armazenar as configurações personalizadas do modo noturno para cada usuário"""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='config_modo_noturno')
    ativo = models.BooleanField(default=False)  # Se o modo noturno está ativo
    
    # Configurações de filtro de luz azul
    filtro_luz_azul_ativo = models.BooleanField(default=True)  # Se o filtro de luz azul está ativo
    intensidade_filtro = models.IntegerField(default=50, help_text='Intensidade do filtro de 0 a 100')  # Intensidade do filtro
    
    # Configurações do modo não perturbe
    nao_perturbe_ativo = models.BooleanField(default=False)  # Se o modo não perturbe está ativo
    horario_inicio = models.TimeField(default=timezone.now)  # Horário de início do modo não perturbe
    horario_fim = models.TimeField(default=timezone.now)  # Horário de fim do modo não perturbe
    silenciar_notificacoes = models.BooleanField(default=True)  # Se deve silenciar notificações
    permitir_chamadas_emergencia = models.BooleanField(default=True)  # Se deve permitir chamadas de emergência
    
    # Configurações de leitura noturna
    leitura_noturna_ativa = models.BooleanField(default=False)  # Se o modo leitura noturna está ativo
    tema_escuro = models.BooleanField(default=True)  # Se o tema escuro está ativo
    tamanho_fonte = models.IntegerField(default=16)  # Tamanho da fonte para leitura
    contraste = models.IntegerField(default=50, help_text='Contraste de 0 a 100')  # Contraste da tela
    
    # Configurações de ativação automática
    ativacao_automatica = models.BooleanField(default=False)  # Se a ativação automática está ativa
    horario_ativacao = models.TimeField(default=timezone.now)  # Horário de ativação automática
    horario_desativacao = models.TimeField(default=timezone.now)  # Horário de desativação automática
    
    data_atualizacao = models.DateTimeField(auto_now=True)  # Data da última atualização
    
    class Meta:
        verbose_name = 'Configuração do Modo Noturno'
        verbose_name_plural = 'Configurações do Modo Noturno'
    
    def __str__(self):
        status = 'Ativo' if self.ativo else 'Inativo'
        return f'Modo Noturno de {self.usuario.username} - {status}'

# Modelo para histórico de uso do modo noturno
class HistoricoModoNoturno(models.Model):
    """Modelo para armazenar o histórico de uso do modo noturno pelo usuário"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historico_modo_noturno')
    data_hora_ativacao = models.DateTimeField()  # Data e hora da ativação
    data_hora_desativacao = models.DateTimeField(blank=True, null=True)  # Data e hora da desativação
    duracao_minutos = models.IntegerField(blank=True, null=True)  # Duração em minutos
    ativado_automaticamente = models.BooleanField(default=False)  # Se foi ativado automaticamente
    
    class Meta:
        verbose_name = 'Histórico do Modo Noturno'
        verbose_name_plural = 'Históricos do Modo Noturno'
        ordering = ['-data_hora_ativacao']
    
    def __str__(self):
        return f'Uso do Modo Noturno por {self.usuario.username} em {self.data_hora_ativacao.strftime("%d/%m/%Y %H:%M")}'
    
    def save(self, *args, **kwargs):
        # Calcula a duração em minutos se houver data de desativação
        if self.data_hora_desativacao:
            delta = self.data_hora_desativacao - self.data_hora_ativacao
            self.duracao_minutos = int(delta.total_seconds() / 60)
        super().save(*args, **kwargs)
