from django import forms
from django.utils import timezone
from .models import Tarefa, Lembrete, ServicoBaba
from rede_apoio.models import ContatoEmergencial

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['descricao', 'prazo', 'prioridade']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da tarefa'}),
            'prazo': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Definir valor mínimo para o prazo (data atual)
        self.fields['prazo'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

class LembreteForm(forms.ModelForm):
    class Meta:
        model = Lembrete
        fields = ['titulo', 'descricao', 'data_notificacao', 'tipo', 'tarefa']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do lembrete'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descrição do lembrete'}),
            'data_notificacao': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'tarefa': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Definir valor mínimo para a data de notificação (data atual)
        self.fields['data_notificacao'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')
        
        # Filtrar tarefas pelo usuário atual
        if user:
            self.fields['tarefa'].queryset = Tarefa.objects.filter(usuario=user, status='pendente')
        else:
            self.fields['tarefa'].queryset = Tarefa.objects.none()

class ServicoBabaForm(forms.ModelForm):
    class Meta:
        model = ServicoBaba
        fields = ['tipo_servico', 'data', 'horario_inicio', 'horario_fim', 'local', 'observacoes', 'contato']
        widgets = {
            'tipo_servico': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'horario_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'horario_fim': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do serviço'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observações adicionais'}),
            'contato': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Definir valor mínimo para a data (data atual)
        self.fields['data'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%d')
        
        # Filtrar contatos pelo usuário atual
        if user:
            self.fields['contato'].queryset = ContatoEmergencial.objects.filter(usuario=user, tipo='cuidador')
        else:
            self.fields['contato'].queryset = ContatoEmergencial.objects.none()
    
    def clean(self):
        cleaned_data = super().clean()
        horario_inicio = cleaned_data.get('horario_inicio')
        horario_fim = cleaned_data.get('horario_fim')
        
        # Verificar se o horário de término é posterior ao horário de início
        if horario_inicio and horario_fim and horario_inicio >= horario_fim:
            self.add_error('horario_fim', 'O horário de término deve ser posterior ao horário de início.')
        
        return cleaned_data