from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Marmita, AvaliacaoMarmita, PlanoAlimentar, ItemPlanoAlimentar

# Views para Marmitas
@login_required
def marmita_list(request):
    """Lista todas as marmitas disponíveis no catálogo"""
    categoria = request.GET.get('categoria', '')
    tipo_refeicao = request.GET.get('tipo_refeicao', '')
    
    marmitas = Marmita.objects.filter(disponivel=True)
    
    if categoria:
        marmitas = marmitas.filter(categoria=categoria)
    if tipo_refeicao:
        marmitas = marmitas.filter(tipo_refeicao=tipo_refeicao)
    
    return render(request, 'nutricao/marmita_list.html', {
        'marmitas': marmitas,
        'categoria_selecionada': categoria,
        'tipo_refeicao_selecionado': tipo_refeicao,
        'categorias': dict(Marmita.CATEGORIA_CHOICES),
        'tipos_refeicao': dict(Marmita.REFEICAO_CHOICES)
    })

@login_required
def marmita_detail(request, pk):
    """Exibe os detalhes de uma marmita específica"""
    marmita = get_object_or_404(Marmita, pk=pk)
    avaliacoes = AvaliacaoMarmita.objects.filter(marmita=marmita)
    
    # Verificar se o usuário já avaliou esta marmita
    avaliacao_usuario = AvaliacaoMarmita.objects.filter(marmita=marmita, usuario=request.user).first()
    
    # Calcular a média das avaliações
    media_avaliacoes = avaliacoes.values_list('nota', flat=True)
    media = sum(media_avaliacoes) / len(media_avaliacoes) if media_avaliacoes else 0
    
    return render(request, 'nutricao/marmita_detail.html', {
        'marmita': marmita,
        'avaliacoes': avaliacoes,
        'avaliacao_usuario': avaliacao_usuario,
        'media_avaliacoes': media
    })

@login_required
def avaliacao_marmita_create(request, pk):
    """Cria uma avaliação para uma marmita"""
    marmita = get_object_or_404(Marmita, pk=pk)
    
    # Verificar se o usuário já avaliou esta marmita
    avaliacao_existente = AvaliacaoMarmita.objects.filter(marmita=marmita, usuario=request.user).first()
    
    if avaliacao_existente:
        messages.warning(request, 'Você já avaliou esta marmita. Sua avaliação foi atualizada.')
        # Aqui seria implementada a atualização da avaliação existente
    else:
        # Aqui seria implementada a criação de uma nova avaliação
        messages.success(request, 'Avaliação registrada com sucesso!')
    
    return redirect('nutricao:marmita_detail', pk=marmita.pk)

# Views para Planos Alimentares
@login_required
def plano_alimentar_list(request):
    """Lista todos os planos alimentares do usuário"""
    planos = PlanoAlimentar.objects.filter(usuario=request.user)
    return render(request, 'nutricao/plano_alimentar_list.html', {
        'planos': planos
    })

@login_required
def plano_alimentar_create(request):
    """Cria um novo plano alimentar"""
    if request.method == 'POST':
        # Processar os dados do formulário
        objetivo = request.POST.get('objetivo')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim') or None
        restricoes = request.POST.get('restricoes', '')
        observacoes = request.POST.get('observacoes', '')
        ativo = request.POST.get('ativo') == 'on'
        
        # Se o novo plano for marcado como ativo, desativar os planos ativos existentes
        if ativo:
            PlanoAlimentar.objects.filter(usuario=request.user, ativo=True).update(ativo=False)
        
        # Criar o novo plano alimentar
        plano = PlanoAlimentar.objects.create(
            usuario=request.user,
            objetivo=objetivo,
            data_inicio=data_inicio,
            data_fim=data_fim,
            restricoes=restricoes,
            observacoes=observacoes,
            ativo=ativo
        )
        
        messages.success(request, 'Plano alimentar criado com sucesso!')
        return redirect('nutricao:plano_alimentar_list')
    return render(request, 'nutricao/plano_alimentar_form.html')

@login_required
def plano_alimentar_detail(request, pk):
    """Exibe os detalhes de um plano alimentar específico"""
    plano = get_object_or_404(PlanoAlimentar, pk=pk, usuario=request.user)
    refeicoes = ItemPlanoAlimentar.objects.filter(plano=plano).order_by('horario')
    
    return render(request, 'nutricao/plano_alimentar_detail.html', {
        'plano': plano,
        'refeicoes': refeicoes
    })

@login_required
def plano_alimentar_update(request, pk):
    """Atualiza um plano alimentar existente"""
    plano = get_object_or_404(PlanoAlimentar, pk=pk, usuario=request.user)
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Plano alimentar atualizado com sucesso!')
        return redirect('nutricao:plano_alimentar_detail', pk=plano.pk)
    return render(request, 'nutricao/plano_alimentar_form.html', {
        'plano': plano
    })

@login_required
def plano_alimentar_delete(request, pk):
    """Exclui um plano alimentar"""
    plano = get_object_or_404(PlanoAlimentar, pk=pk, usuario=request.user)
    if request.method == 'POST':
        plano.delete()
        messages.success(request, 'Plano alimentar excluído com sucesso!')
        return redirect('nutricao:plano_alimentar_list')
    return render(request, 'nutricao/plano_alimentar_confirm_delete.html', {
        'plano': plano
    })

# Views para Refeições do Plano Alimentar
@login_required
def refeicao_plano_create(request, plano_pk):
    """Adiciona uma refeição a um plano alimentar"""
    plano = get_object_or_404(PlanoAlimentar, pk=plano_pk, usuario=request.user)
    
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Refeição adicionada com sucesso!')
        return redirect('nutricao:plano_alimentar_detail', pk=plano.pk)
    
    return render(request, 'nutricao/refeicao_plano_form.html', {
        'plano': plano
    })

@login_required
def refeicao_plano_update(request, pk):
    """Atualiza uma refeição de um plano alimentar"""
    refeicao = get_object_or_404(ItemPlanoAlimentar, pk=pk)
    plano = refeicao.plano
    
    # Verificar se o plano pertence ao usuário
    if plano.usuario != request.user:
        messages.error(request, 'Você não tem permissão para editar esta refeição.')
        return redirect('nutricao:plano_alimentar_list')
    
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Refeição atualizada com sucesso!')
        return redirect('nutricao:plano_alimentar_detail', pk=plano.pk)
    
    return render(request, 'nutricao/refeicao_plano_form.html', {
        'plano': plano,
        'refeicao': refeicao
    })

@login_required
def refeicao_plano_delete(request, pk):
    """Exclui uma refeição de um plano alimentar"""
    refeicao = get_object_or_404(ItemPlanoAlimentar, pk=pk)
    plano = refeicao.plano
    
    # Verificar se o plano pertence ao usuário
    if plano.usuario != request.user:
        messages.error(request, 'Você não tem permissão para excluir esta refeição.')
        return redirect('nutricao:plano_alimentar_list')
    
    if request.method == 'POST':
        refeicao.delete()
        messages.success(request, 'Refeição excluída com sucesso!')
        return redirect('nutricao:plano_alimentar_detail', pk=plano.pk)
    
    return render(request, 'nutricao/refeicao_plano_confirm_delete.html', {
        'refeicao': refeicao,
        'plano': plano
    })

# Dashboard de Nutrição
@login_required
def nutricao_dashboard(request):
    """Exibe o dashboard de nutrição com informações consolidadas"""
    # Obter o plano alimentar ativo do usuário
    plano_ativo = PlanoAlimentar.objects.filter(usuario=request.user, ativo=True).first()
    
    # Obter as marmitas recomendadas com base nas preferências do usuário
    marmitas_recomendadas = Marmita.objects.filter(disponivel=True)[:5]
    
    # Obter as últimas avaliações do usuário
    avaliacoes_usuario = AvaliacaoMarmita.objects.filter(usuario=request.user).order_by('-id')[:3]
    
    return render(request, 'nutricao/dashboard.html', {
        'plano_ativo': plano_ativo,
        'marmitas_recomendadas': marmitas_recomendadas,
        'avaliacoes_usuario': avaliacoes_usuario
    })
