from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from .models import Tarefa, Lembrete, ServicoBaba
from educacional.models import Evento
from rede_apoio.models import ContatoEmergencial
from .forms import TarefaForm, LembreteForm, ServicoBabaForm

# Views para Tarefas
class TarefaListView(LoginRequiredMixin, ListView):
    model = Tarefa
    template_name = 'tarefas/tarefa_list.html'
    context_object_name = 'tarefas'
    
    def get_queryset(self):
        queryset = Tarefa.objects.filter(usuario=self.request.user)
        
        # Filtrar por status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filtrar por prioridade
        prioridade = self.request.GET.get('prioridade', '')
        if prioridade:
            queryset = queryset.filter(prioridade=prioridade)
        
        # Buscar por descrição
        busca = self.request.GET.get('busca', '')
        if busca:
            queryset = queryset.filter(descricao__icontains=busca)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_selecionado'] = self.request.GET.get('status', '')
        context['prioridade_selecionada'] = self.request.GET.get('prioridade', '')
        context['busca'] = self.request.GET.get('busca', '')
        context['form'] = TarefaForm()
        return context

class TarefaCreateView(LoginRequiredMixin, CreateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'tarefas/tarefa_form.html'
    success_url = reverse_lazy('tarefas:tarefa_list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Tarefa criada com sucesso!')
        return super().form_valid(form)

class TarefaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'tarefas/tarefa_form.html'
    success_url = reverse_lazy('tarefas:tarefa_list')
    
    def get_queryset(self):
        return Tarefa.objects.filter(usuario=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Tarefa atualizada com sucesso!')
        return super().form_valid(form)

class TarefaDeleteView(LoginRequiredMixin, DeleteView):
    model = Tarefa
    template_name = 'tarefas/tarefa_confirm_delete.html'
    success_url = reverse_lazy('tarefas:tarefa_list')
    
    def get_queryset(self):
        return Tarefa.objects.filter(usuario=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Tarefa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

@login_required
def tarefa_concluir(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    tarefa.concluir()
    messages.success(request, 'Tarefa marcada como concluída!')
    return redirect('tarefas:tarefa_list')

@login_required
def tarefa_adicionar_calendario(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk, usuario=request.user)
    
    # Criar um evento associado à tarefa
    evento = Evento(
        usuario=request.user,
        titulo=f'Tarefa: {tarefa.descricao}',
        descricao=f'Prazo para a tarefa: {tarefa.descricao}',
        data_inicio=tarefa.prazo,
        data_fim=tarefa.prazo,
        lembrete=True,
        tempo_lembrete=30
    )
    evento.save()
    
    # Associar o evento à tarefa
    tarefa.evento = evento
    tarefa.save()
    
    messages.success(request, 'Tarefa adicionada ao calendário com sucesso!')
    return redirect('tarefas:tarefa_list')

# Views para Calendário
class CalendarioView(LoginRequiredMixin, TemplateView):
    template_name = 'tarefas/calendario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obter eventos do usuário
        eventos = Evento.objects.filter(usuario=self.request.user)
        
        # Obter tarefas sem eventos associados
        tarefas = Tarefa.objects.filter(usuario=self.request.user, evento__isnull=True)
        
        context['eventos'] = eventos
        context['tarefas'] = tarefas
        return context

@login_required
def calendario_eventos_json(request):
    # Obter eventos do usuário
    eventos = Evento.objects.filter(usuario=request.user)
    
    # Formatar eventos para o calendário
    eventos_json = []
    for evento in eventos:
        eventos_json.append({
            'id': evento.id,
            'title': evento.titulo,
            'start': evento.data_inicio.isoformat(),
            'end': evento.data_fim.isoformat() if evento.data_fim else evento.data_inicio.isoformat(),
            'color': '#007bff',  # Azul para eventos
            'url': f'/educacional/eventos/{evento.id}/'
        })
    
    # Obter tarefas do usuário
    tarefas = Tarefa.objects.filter(usuario=request.user, status='pendente')
    
    # Formatar tarefas para o calendário
    for tarefa in tarefas:
        cor = '#dc3545'  # Vermelho para tarefas de alta prioridade
        if tarefa.prioridade == 'media':
            cor = '#ffc107'  # Amarelo para tarefas de média prioridade
        elif tarefa.prioridade == 'baixa':
            cor = '#28a745'  # Verde para tarefas de baixa prioridade
        
        eventos_json.append({
            'id': f'tarefa_{tarefa.id}',
            'title': f'Tarefa: {tarefa.descricao}',
            'start': tarefa.prazo.isoformat(),
            'end': tarefa.prazo.isoformat(),
            'color': cor,
            'url': f'/tarefas/{tarefa.id}/'
        })
    
    # Obter serviços de babá do usuário
    servicos = ServicoBaba.objects.filter(usuario=request.user, status='agendado')
    
    # Formatar serviços para o calendário
    for servico in servicos:
        data_inicio = timezone.datetime.combine(servico.data, servico.horario_inicio)
        data_fim = timezone.datetime.combine(servico.data, servico.horario_fim)
        
        eventos_json.append({
            'id': f'servico_{servico.id}',
            'title': f'Babá: {servico.get_tipo_servico_display()}',
            'start': data_inicio.isoformat(),
            'end': data_fim.isoformat(),
            'color': '#6f42c1',  # Roxo para serviços de babá
            'url': f'/tarefas/babas/{servico.id}/'
        })
    
    return JsonResponse(eventos_json, safe=False)

# Views para Lembretes
class LembreteListView(LoginRequiredMixin, ListView):
    model = Lembrete
    template_name = 'tarefas/lembrete_list.html'
    context_object_name = 'lembretes'
    
    def get_queryset(self):
        return Lembrete.objects.filter(usuario=self.request.user)

class LembreteCreateView(LoginRequiredMixin, CreateView):
    model = Lembrete
    form_class = LembreteForm
    template_name = 'tarefas/lembrete_form.html'
    success_url = reverse_lazy('tarefas:lembrete_list')
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        messages.success(self.request, 'Lembrete criado com sucesso!')
        return super().form_valid(form)

@login_required
def lembrete_marcar_lido(request, pk):
    lembrete = get_object_or_404(Lembrete, pk=pk, usuario=request.user)
    lembrete.marcar_como_lido()
    messages.success(request, 'Lembrete marcado como lido!')
    return redirect('tarefas:lembrete_list')

@login_required
def lembretes_nao_lidos(request):
    lembretes = Lembrete.objects.filter(usuario=request.user, lido=False).order_by('-data_notificacao')
    
    lembretes_json = []
    for lembrete in lembretes:
        lembretes_json.append({
            'id': lembrete.id,
            'titulo': lembrete.titulo,
            'tipo': lembrete.get_tipo_display(),
            'data': lembrete.data_notificacao.strftime('%d/%m/%Y %H:%M'),
            'url': f'/tarefas/lembretes/{lembrete.id}/'
        })
    
    return JsonResponse({
        'count': lembretes.count(),
        'lembretes': lembretes_json
    })

# Views para Serviço de Babás
class ServicoBabaListView(LoginRequiredMixin, ListView):
    model = ServicoBaba
    template_name = 'tarefas/servico_baba_list.html'
    context_object_name = 'servicos'
    
    def get_queryset(self):
        return ServicoBaba.objects.filter(usuario=self.request.user)

class ServicoBabaCreateView(LoginRequiredMixin, CreateView):
    model = ServicoBaba
    form_class = ServicoBabaForm
    template_name = 'tarefas/servico_baba_form.html'
    success_url = reverse_lazy('tarefas:servico_baba_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
        # Criar um evento associado ao serviço de babá
        data = form.cleaned_data['data']
        horario_inicio = form.cleaned_data['horario_inicio']
        horario_fim = form.cleaned_data['horario_fim']
        
        data_inicio = timezone.datetime.combine(data, horario_inicio)
        data_fim = timezone.datetime.combine(data, horario_fim)
        
        evento = Evento(
            usuario=self.request.user,
            titulo=f'Serviço de Babá: {form.cleaned_data["tipo_servico"]}',
            descricao=f'Local: {form.cleaned_data["local"]}\nObservações: {form.cleaned_data["observacoes"]}',
            data_inicio=data_inicio,
            data_fim=data_fim,
            local=form.cleaned_data['local'],
            lembrete=True,
            tempo_lembrete=60
        )
        evento.save()
        
        # Associar o evento ao serviço de babá
        form.instance.evento = evento
        
        messages.success(self.request, 'Serviço de babá agendado com sucesso!')
        return super().form_valid(form)

class ServicoBabaDetailView(LoginRequiredMixin, DetailView):
    model = ServicoBaba
    template_name = 'tarefas/servico_baba_detail.html'
    context_object_name = 'servico'
    
    def get_queryset(self):
        return ServicoBaba.objects.filter(usuario=self.request.user)

@login_required
def servico_baba_cancelar(request, pk):
    servico = get_object_or_404(ServicoBaba, pk=pk, usuario=request.user)
    servico.cancelar()
    messages.success(request, 'Serviço de babá cancelado com sucesso!')
    return redirect('tarefas:servico_baba_list')

@login_required
def servico_baba_contatar(request, pk):
    servico = get_object_or_404(ServicoBaba, pk=pk, usuario=request.user)
    
    if not servico.contato:
        messages.error(request, 'Este serviço não possui um contato associado.')
        return redirect('tarefas:servico_baba_detail', pk=servico.pk)
    
    # Redirecionar para WhatsApp ou outra forma de contato
    telefone = servico.contato.telefone.replace('+', '').replace('-', '').replace(' ', '')
    whatsapp_url = f'https://wa.me/{telefone}?text=Olá%20{servico.contato.nome},%20gostaria%20de%20confirmar%20o%20serviço%20de%20babá%20para%20o%20dia%20{servico.data.strftime("%d/%m/%Y")}%20das%20{servico.horario_inicio.strftime("%H:%M")}%20às%20{servico.horario_fim.strftime("%H:%M")}'