from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import ConfiguracaoModoNoturno, HistoricoModoNoturno

# Views para Configuração do Modo Noturno
@login_required
def configuracao_detail(request):
    """Exibe os detalhes da configuração do modo noturno do usuário"""
    try:
        config = ConfiguracaoModoNoturno.objects.get(usuario=request.user)
    except ConfiguracaoModoNoturno.DoesNotExist:
        config = ConfiguracaoModoNoturno.objects.create(usuario=request.user)
    
    return render(request, 'modo_noturno/configuracao_detail.html', {
        'config': config
    })

@login_required
def configuracao_update(request):
    """Atualiza a configuração do modo noturno do usuário"""
    try:
        config = ConfiguracaoModoNoturno.objects.get(usuario=request.user)
    except ConfiguracaoModoNoturno.DoesNotExist:
        config = ConfiguracaoModoNoturno.objects.create(usuario=request.user)
    
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Configurações do modo noturno atualizadas com sucesso!')
        return redirect('modo_noturno:configuracao')
    
    return render(request, 'modo_noturno/configuracao_form.html', {
        'config': config
    })

@login_required
def modo_noturno_toggle(request):
    """Ativa ou desativa o modo noturno"""
    try:
        config = ConfiguracaoModoNoturno.objects.get(usuario=request.user)
    except ConfiguracaoModoNoturno.DoesNotExist:
        config = ConfiguracaoModoNoturno.objects.create(usuario=request.user)
    
    # Inverter o estado atual
    config.ativo = not config.ativo
    config.save()
    
    # Registrar o uso no histórico
    HistoricoModoNoturno.objects.create(
        usuario=request.user,
        acao='ativacao' if config.ativo else 'desativacao'
    )
    
    if request.is_ajax():
        return JsonResponse({'status': 'success', 'ativo': config.ativo})
    
    messages.success(request, f'Modo noturno {"ativado" if config.ativo else "desativado"} com sucesso!')
    return redirect('modo_noturno:configuracao')

@login_required
def historico_list(request):
    """Lista o histórico de uso do modo noturno"""
    historico = HistoricoModoNoturno.objects.filter(usuario=request.user).order_by('-data_hora')
    return render(request, 'modo_noturno/historico_list.html', {
        'historico': historico
    })

@login_required
def configuracao_avancada(request):
    """Exibe e processa as configurações avançadas do modo noturno"""
    try:
        config = ConfiguracaoModoNoturno.objects.get(usuario=request.user)
    except ConfiguracaoModoNoturno.DoesNotExist:
        config = ConfiguracaoModoNoturno.objects.create(usuario=request.user)
    
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Configurações avançadas atualizadas com sucesso!')
        return redirect('modo_noturno:configuracao')
    
    return render(request, 'modo_noturno/configuracao_avancada.html', {
        'config': config
    })

@login_required
def estatisticas(request):
    """Exibe estatísticas de uso do modo noturno"""
    # Obter a configuração do usuário
    try:
        config = ConfiguracaoModoNoturno.objects.get(usuario=request.user)
    except ConfiguracaoModoNoturno.DoesNotExist:
        config = ConfiguracaoModoNoturno.objects.create(usuario=request.user)
    
    # Obter o histórico de uso
    historico = HistoricoModoNoturno.objects.filter(usuario=request.user)
    
    # Calcular estatísticas
    total_ativacoes = historico.filter(acao='ativacao').count()
    total_desativacoes = historico.filter(acao='desativacao').count()
    
    # Calcular o tempo médio de uso (em horas)
    tempo_total = 0
    contagem_periodos = 0
    
    ativacoes = list(historico.filter(acao='ativacao').order_by('data_hora'))
    desativacoes = list(historico.filter(acao='desativacao').order_by('data_hora'))
    
    for i, ativacao in enumerate(ativacoes):
        # Procurar a próxima desativação após esta ativação
        for desativacao in desativacoes:
            if desativacao.data_hora > ativacao.data_hora:
                # Calcular a diferença de tempo
                diferenca = desativacao.data_hora - ativacao.data_hora
                tempo_total += diferenca.total_seconds() / 3600  # Converter para horas
                contagem_periodos += 1
                break
    
    tempo_medio = tempo_total / contagem_periodos if contagem_periodos > 0 else 0
    
    return render(request, 'modo_noturno/estatisticas.html', {
        'config': config,
        'total_ativacoes': total_ativacoes,
        'total_desativacoes': total_desativacoes,
        'tempo_medio': tempo_medio
    })
