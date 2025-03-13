from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.db import models
from .models import AtividadeFisica, ConsumoAgua, MetaAgua, MonitoramentoSaude
from django.db.models import Sum

# Views para Atividade Física
@login_required
def atividade_fisica_list(request):
    """Lista todas as atividades físicas do usuário logado"""
    atividades = AtividadeFisica.objects.filter(usuario=request.user)
    return render(request, 'saude/atividade_fisica_list.html', {
        'atividades': atividades
    })

@login_required
def atividade_fisica_create(request):
    """Cria uma nova atividade física"""
    if request.method == 'POST':
        # Processar os dados do formulário
        tipo = request.POST.get('tipo')
        data = request.POST.get('data')
        duracao = request.POST.get('duracao')
        calorias_gastas = request.POST.get('calorias_gastas')
        descricao = request.POST.get('descricao')
        
        # Criar nova atividade física
        atividade = AtividadeFisica(
            usuario=request.user,
            tipo=tipo,
            data=data,
            duracao=duracao,
            descricao=descricao
        )
        
        # Adicionar calorias gastas se fornecido
        if calorias_gastas:
            atividade.calorias_gastas = calorias_gastas
        
        # Salvar a atividade no banco de dados
        atividade.save()
        
        messages.success(request, 'Atividade física registrada com sucesso!')
        return redirect('saude:atividade_fisica_list')
    return render(request, 'saude/atividade_fisica_form.html')

@login_required
def atividade_fisica_detail(request, pk):
    """Exibe os detalhes de uma atividade física específica"""
    atividade = get_object_or_404(AtividadeFisica, pk=pk, usuario=request.user)
    return render(request, 'saude/atividade_fisica_detail.html', {
        'atividade': atividade
    })

@login_required
def atividade_fisica_update(request, pk):
    """Atualiza uma atividade física existente"""
    atividade = get_object_or_404(AtividadeFisica, pk=pk, usuario=request.user)
    if request.method == 'POST':
        # Processar os dados do formulário
        atividade.tipo = request.POST.get('tipo')
        atividade.data = request.POST.get('data')
        atividade.duracao = request.POST.get('duracao')
        atividade.descricao = request.POST.get('descricao')
        
        # Atualizar calorias gastas se fornecido
        calorias_gastas = request.POST.get('calorias_gastas')
        if calorias_gastas:
            atividade.calorias_gastas = calorias_gastas
        else:
            atividade.calorias_gastas = None
        
        # Salvar as alterações no banco de dados
        atividade.save()
        
        messages.success(request, 'Atividade física atualizada com sucesso!')
        return redirect('saude:atividade_fisica_detail', pk=atividade.pk)
    return render(request, 'saude/atividade_fisica_form.html', {
        'atividade': atividade
    })

@login_required
def atividade_fisica_delete(request, pk):
    """Exclui uma atividade física"""
    atividade = get_object_or_404(AtividadeFisica, pk=pk, usuario=request.user)
    if request.method == 'POST':
        atividade.delete()
        messages.success(request, 'Atividade física excluída com sucesso!')
        return redirect('saude:atividade_fisica_list')
    return render(request, 'saude/atividade_fisica_confirm_delete.html', {
        'atividade': atividade
    })

# Views para Consumo de Água
@login_required
def consumo_agua_list(request):
    """Lista todos os registros de consumo de água do usuário logado"""
    hoje = timezone.now().date()
    consumos = ConsumoAgua.objects.filter(usuario=request.user)
    consumos_hoje = consumos.filter(data=hoje)
    
    # Calcular o total consumido hoje
    total_hoje = consumos_hoje.aggregate(total=Sum('quantidade_ml'))['total'] or 0
    
    # Obter a meta diária do usuário
    try:
        meta_agua = MetaAgua.objects.get(usuario=request.user)
        meta_diaria = meta_agua.quantidade_diaria_ml
    except MetaAgua.DoesNotExist:
        meta_diaria = 2000  # Valor padrão
        meta_agua = None
    
    # Calcular a porcentagem da meta atingida
    porcentagem = min(int((total_hoje / meta_diaria) * 100), 100) if meta_diaria > 0 else 0
    
    return render(request, 'saude/consumo_agua_list.html', {
        'consumos': consumos,
        'consumos_hoje': consumos_hoje,
        'total_hoje': total_hoje,
        'meta_diaria': meta_diaria,
        'porcentagem': porcentagem,
        'meta_agua': meta_agua
    })

@login_required
def consumo_agua_create(request):
    """Registra um novo consumo de água"""
    if request.method == 'POST':
        # Processar os dados do formulário
        quantidade = request.POST.get('quantidade')
        data_hora = request.POST.get('data_hora')
        observacoes = request.POST.get('observacoes')
        
        # Criar novo registro de consumo
        data = timezone.datetime.strptime(data_hora, '%Y-%m-%dT%H:%M').date()
        horario = timezone.datetime.strptime(data_hora, '%Y-%m-%dT%H:%M').time()
        
        consumo = ConsumoAgua(
            usuario=request.user,
            quantidade_ml=quantidade,
            data=data,
            horario=horario,
            observacoes=observacoes if observacoes else None
        )
        
        # Salvar o consumo no banco de dados
        consumo.save()
        
        # Calcular o total consumido hoje
        hoje = timezone.now().date()
        consumos_hoje = ConsumoAgua.objects.filter(usuario=request.user, data=hoje)
        total_hoje = consumos_hoje.aggregate(total=Sum('quantidade_ml'))['total'] or 0
        
        # Obter a meta diária do usuário
        try:
            meta_agua = MetaAgua.objects.get(usuario=request.user)
            meta_diaria = meta_agua.quantidade_diaria_ml
        except MetaAgua.DoesNotExist:
            meta_diaria = 2000  # Valor padrão
        
        # Calcular a porcentagem da meta atingida
        porcentagem = min(int((total_hoje / meta_diaria) * 100), 100) if meta_diaria > 0 else 0
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': 'Consumo de água registrado com sucesso!',
                'total_hoje': total_hoje,
                'meta_diaria': meta_diaria,
                'porcentagem': porcentagem,
                'consumos_hoje': [{
                    'quantidade_ml': c.quantidade_ml,
                    'horario': c.horario.strftime('%H:%M'),
                    'id': c.id
                } for c in consumos_hoje]
            })
        
        messages.success(request, 'Consumo de água registrado com sucesso!')
        return redirect('saude:consumo_agua_list')
    return render(request, 'saude/consumo_agua_form.html')

@login_required
def consumo_agua_detail(request, pk):
    """Exibe os detalhes de um registro de consumo de água"""
    consumo = get_object_or_404(ConsumoAgua, pk=pk, usuario=request.user)
    return render(request, 'saude/consumo_agua_detail.html', {
        'consumo': consumo
    })

@login_required
def consumo_agua_update(request, pk):
    """Atualiza um registro de consumo de água"""
    consumo = get_object_or_404(ConsumoAgua, pk=pk, usuario=request.user)
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Consumo de água atualizado com sucesso!')
        return redirect('saude:consumo_agua_detail', pk=consumo.pk)
    return render(request, 'saude/consumo_agua_form.html', {
        'consumo': consumo
    })

@login_required
def consumo_agua_delete(request, pk):
    """Exclui um registro de consumo de água"""
    consumo = get_object_or_404(ConsumoAgua, pk=pk, usuario=request.user)
    if request.method == 'POST':
        consumo.delete()
        messages.success(request, 'Consumo de água excluído com sucesso!')
        return redirect('saude:consumo_agua_list')
    return render(request, 'saude/consumo_agua_confirm_delete.html', {
        'consumo': consumo
    })

# Views para Meta de Água
@login_required
def meta_agua_detail(request):
    """Exibe os detalhes da meta de água do usuário"""
    try:
        meta_agua = MetaAgua.objects.get(usuario=request.user)
    except MetaAgua.DoesNotExist:
        meta_agua = MetaAgua.objects.create(usuario=request.user)
    
    # Calcular o consumo de hoje
    hoje = timezone.now().date()
    consumos_hoje = ConsumoAgua.objects.filter(usuario=request.user, data=hoje)
    consumido_hoje = consumos_hoje.aggregate(total=Sum('quantidade_ml'))['total'] or 0
    
    # Calcular o percentual consumido
    percentual_consumido = min(int((consumido_hoje / meta_agua.quantidade_diaria_ml) * 100), 100) if meta_agua.quantidade_diaria_ml > 0 else 0
    
    # Obter os consumos recentes
    consumos_recentes = ConsumoAgua.objects.filter(usuario=request.user).order_by('-data', '-horario')[:5]
    
    return render(request, 'saude/meta_agua_detail.html', {
        'meta_agua': meta_agua,
        'consumido_hoje': consumido_hoje,
        'percentual_consumido': percentual_consumido,
        'consumos_recentes': consumos_recentes
    })

@login_required
def meta_agua_update(request):
    """Atualiza a meta de água do usuário"""
    try:
        meta_agua = MetaAgua.objects.get(usuario=request.user)
    except MetaAgua.DoesNotExist:
        meta_agua = MetaAgua.objects.create(usuario=request.user)
    
    if request.method == 'POST':
        # Processar os dados do formulário
        quantidade_diaria = request.POST.get('meta_ml')
        observacoes = request.POST.get('observacoes')
        
        # Atualizar a meta de água
        meta_agua.quantidade_diaria_ml = quantidade_diaria
        if observacoes:
            meta_agua.observacoes = observacoes
        meta_agua.save()
        
        messages.success(request, 'Meta de água atualizada com sucesso!')
        return redirect('saude:meta_agua_detail')
    
    return render(request, 'saude/meta_agua_form.html', {
        'meta_agua': meta_agua
    })

# Views para Monitoramento de Saúde
@login_required
def monitoramento_saude_list(request):
    """Lista todos os registros de monitoramento de saúde do usuário"""
    monitoramentos = MonitoramentoSaude.objects.filter(usuario=request.user).order_by('-data')
    
    # Obter o último monitoramento para exibir métricas atuais
    ultimo_monitoramento = monitoramentos.first()
    
    # Calcular médias para comparação
    media_passos = monitoramentos.exclude(passos__isnull=True).aggregate(models.Avg('passos'))['passos__avg'] or 0
    media_sono = monitoramentos.exclude(horas_sono__isnull=True).aggregate(models.Avg('horas_sono'))['horas_sono__avg'] or 0
    media_calorias = monitoramentos.exclude(calorias_gastas__isnull=True).aggregate(models.Avg('calorias_gastas'))['calorias_gastas__avg'] or 0
    media_freq_cardiaca = monitoramentos.exclude(frequencia_cardiaca_media__isnull=True).aggregate(models.Avg('frequencia_cardiaca_media'))['frequencia_cardiaca_media__avg'] or 0
    
    # Calcular variações percentuais
    var_passos = ((ultimo_monitoramento.passos / media_passos - 1) * 100) if ultimo_monitoramento and ultimo_monitoramento.passos and media_passos else 0
    var_sono = ((ultimo_monitoramento.horas_sono / media_sono - 1) * 100) if ultimo_monitoramento and ultimo_monitoramento.horas_sono and media_sono else 0
    var_calorias = ((ultimo_monitoramento.calorias_gastas / media_calorias - 1) * 100) if ultimo_monitoramento and ultimo_monitoramento.calorias_gastas and media_calorias else 0
    var_freq_cardiaca = ((ultimo_monitoramento.frequencia_cardiaca_media / media_freq_cardiaca - 1) * 100) if ultimo_monitoramento and ultimo_monitoramento.frequencia_cardiaca_media and media_freq_cardiaca else 0
    
    context = {
        'monitoramentos': monitoramentos,
        'ultimo_monitoramento': ultimo_monitoramento,
        'var_passos': var_passos,
        'var_sono': var_sono,
        'var_calorias': var_calorias,
        'var_freq_cardiaca': var_freq_cardiaca
    }
    
    return render(request, 'saude/monitoramento_saude_list.html', context)

@login_required
def monitoramento_saude_create(request):
    """Cria um novo registro de monitoramento de saúde"""
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Monitoramento de saúde registrado com sucesso!')
        return redirect('saude:monitoramento_saude_list')
    return render(request, 'saude/monitoramento_saude_form.html')

@login_required
def monitoramento_saude_detail(request, pk):
    """Exibe os detalhes de um registro de monitoramento de saúde"""
    monitoramento = get_object_or_404(MonitoramentoSaude, pk=pk, usuario=request.user)
    return render(request, 'saude/monitoramento_saude_detail.html', {
        'monitoramento': monitoramento
    })

@login_required
def monitoramento_saude_update(request, pk):
    """Atualiza um registro de monitoramento de saúde"""
    monitoramento = get_object_or_404(MonitoramentoSaude, pk=pk, usuario=request.user)
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Monitoramento de saúde atualizado com sucesso!')
        return redirect('saude:monitoramento_saude_detail', pk=monitoramento.pk)
    return render(request, 'saude/monitoramento_saude_form.html', {
        'monitoramento': monitoramento
    })

@login_required
def monitoramento_saude_delete(request, pk):
    """Exclui um registro de monitoramento de saúde"""
    monitoramento = get_object_or_404(MonitoramentoSaude, pk=pk, usuario=request.user)
    if request.method == 'POST':
        monitoramento.delete()
        messages.success(request, 'Monitoramento de saúde excluído com sucesso!')
        return redirect('saude:monitoramento_saude_list')
    return render(request, 'saude/monitoramento_saude_confirm_delete.html', {
        'monitoramento': monitoramento
    })

# Dashboard de Saúde
@login_required
def saude_dashboard(request):
    """Exibe o dashboard de saúde com informações consolidadas"""
    hoje = timezone.now().date()
    
    # Obter a última atividade física
    ultima_atividade = AtividadeFisica.objects.filter(usuario=request.user).first()
    
    # Obter o consumo de água de hoje
    consumos_hoje = ConsumoAgua.objects.filter(usuario=request.user, data=hoje)
    total_agua_hoje = consumos_hoje.aggregate(total=Sum('quantidade_ml'))['total'] or 0
    
    # Obter a meta diária de água
    try:
        meta_agua = MetaAgua.objects.get(usuario=request.user)
        meta_diaria = meta_agua.quantidade_diaria_ml
    except MetaAgua.DoesNotExist:
        meta_diaria = 2000  # Valor padrão
    
    # Calcular a porcentagem da meta atingida
    porcentagem_agua = min(int((total_agua_hoje / meta_diaria) * 100), 100) if meta_diaria > 0 else 0
    
    # Obter o último monitoramento de saúde
    ultimo_monitoramento = MonitoramentoSaude.objects.filter(usuario=request.user).first()
    
    return render(request, 'saude/dashboard.html', {
        'ultima_atividade': ultima_atividade,
        'total_agua_hoje': total_agua_hoje,
        'meta_diaria': meta_diaria,
        'porcentagem_agua': porcentagem_agua,
        'ultimo_monitoramento': ultimo_monitoramento
    })
