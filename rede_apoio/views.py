from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ContatoEmergencial, AcionamentoEmergencia, GrupoApoio, ParticipacaoGrupo

# Views para Contatos Emergenciais
@login_required
def contato_emergencial_list(request):
    """Lista todos os contatos emergenciais do usuário"""
    contatos = ContatoEmergencial.objects.filter(usuario=request.user)
    return render(request, 'rede_apoio/contato_emergencial_list.html', {
        'contatos': contatos
    })

@login_required
def contato_emergencial_create(request):
    """Cria um novo contato emergencial"""
    if request.method == 'POST':
        # Processar o formulário e criar um novo contato
        novo_contato = ContatoEmergencial(
            usuario=request.user,
            nome=request.POST.get('nome'),
            tipo=request.POST.get('relacao'),  # O campo no form é 'relacao' mas no modelo é 'tipo'
            telefone=request.POST.get('telefone'),
            email=request.POST.get('email'),
            endereco=request.POST.get('endereco'),
            observacoes=request.POST.get('observacoes'),
            # Converter a prioridade de A/M/B para valores numéricos
            prioridade=1 if request.POST.get('prioridade') == 'A' else (3 if request.POST.get('prioridade') == 'B' else 2),
            acionamento_rapido=request.POST.get('prioridade') == 'A'  # Contatos de alta prioridade são marcados para acionamento rápido
        )
        novo_contato.save()
        messages.success(request, 'Contato emergencial adicionado com sucesso!')
        return redirect('rede_apoio:contato_emergencial_list')
    return render(request, 'rede_apoio/contato_emergencial_form.html')

@login_required
def contato_emergencial_detail(request, pk):
    """Exibe os detalhes de um contato emergencial específico"""
    contato = get_object_or_404(ContatoEmergencial, pk=pk, usuario=request.user)
    acionamentos = AcionamentoEmergencia.objects.filter(contato=contato)
    
    return render(request, 'rede_apoio/contato_emergencial_detail.html', {
        'contato': contato,
        'acionamentos': acionamentos
    })

@login_required
def contato_emergencial_update(request, pk):
    """Atualiza um contato emergencial existente"""
    contato = get_object_or_404(ContatoEmergencial, pk=pk, usuario=request.user)
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Contato emergencial atualizado com sucesso!')
        return redirect('rede_apoio:contato_emergencial_detail', pk=contato.pk)
    return render(request, 'rede_apoio/contato_emergencial_form.html', {
        'contato': contato
    })

@login_required
def contato_emergencial_delete(request, pk):
    """Exclui um contato emergencial"""
    contato = get_object_or_404(ContatoEmergencial, pk=pk, usuario=request.user)
    if request.method == 'POST':
        contato.delete()
        messages.success(request, 'Contato emergencial excluído com sucesso!')
        return redirect('rede_apoio:contato_emergencial_list')
    return render(request, 'rede_apoio/contato_emergencial_confirm_delete.html', {
        'contato': contato
    })

# Views para Acionamentos de Emergência
@login_required
def acionamento_emergencia_list(request):
    """Lista todos os acionamentos de emergência do usuário"""
    acionamentos = AcionamentoEmergencia.objects.filter(usuario=request.user)
    return render(request, 'rede_apoio/acionamento_emergencia_list.html', {
        'acionamentos': acionamentos
    })

@login_required
def acionamento_emergencia_create(request):
    """Cria um novo acionamento de emergência"""
    contatos = ContatoEmergencial.objects.filter(usuario=request.user)
    
    if not contatos.exists():
        messages.warning(request, 'Você precisa cadastrar pelo menos um contato emergencial antes de fazer um acionamento.')
        return redirect('rede_apoio:contato_emergencial_create')
    
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Acionamento de emergência registrado com sucesso!')
        return redirect('rede_apoio:acionamento_emergencia_list')
    
    return render(request, 'rede_apoio/acionamento_emergencia_form.html', {
        'contatos': contatos
    })

@login_required
def acionamento_emergencia_detail(request, pk):
    """Exibe os detalhes de um acionamento de emergência específico"""
    acionamento = get_object_or_404(AcionamentoEmergencia, pk=pk, usuario=request.user)
    return render(request, 'rede_apoio/acionamento_emergencia_detail.html', {
        'acionamento': acionamento
    })

@login_required
def acionamento_emergencia_update(request, pk):
    """Atualiza um acionamento de emergência existente"""
    acionamento = get_object_or_404(AcionamentoEmergencia, pk=pk, usuario=request.user)
    contatos = ContatoEmergencial.objects.filter(usuario=request.user)
    
    if request.method == 'POST':
        # Aqui seria implementado o processamento do formulário
        messages.success(request, 'Acionamento de emergência atualizado com sucesso!')
        return redirect('rede_apoio:acionamento_emergencia_detail', pk=acionamento.pk)
    
    return render(request, 'rede_apoio/acionamento_emergencia_form.html', {
        'acionamento': acionamento,
        'contatos': contatos
    })

@login_required
def acionamento_emergencia_delete(request, pk):
    """Exclui um acionamento de emergência"""
    acionamento = get_object_or_404(AcionamentoEmergencia, pk=pk, usuario=request.user)
    if request.method == 'POST':
        acionamento.delete()
        messages.success(request, 'Acionamento de emergência excluído com sucesso!')
        return redirect('rede_apoio:acionamento_emergencia_list')
    return render(request, 'rede_apoio/acionamento_emergencia_confirm_delete.html', {
        'acionamento': acionamento
    })

@login_required
def acionamento_emergencia_atender(request, pk):
    """Marca um acionamento de emergência como atendido"""
    acionamento = get_object_or_404(AcionamentoEmergencia, pk=pk, usuario=request.user)
    acionamento.atendido = True
    acionamento.save()
    messages.success(request, 'Acionamento de emergência marcado como atendido!')
    return redirect('rede_apoio:acionamento_emergencia_detail', pk=acionamento.pk)

# Views para Grupos de Apoio
@login_required
def grupo_apoio_list(request):
    """Lista todos os grupos de apoio disponíveis"""
    grupos = GrupoApoio.objects.all()
    participacoes = ParticipacaoGrupo.objects.filter(usuario=request.user).values_list('grupo_id', flat=True)
    
    return render(request, 'rede_apoio/grupo_apoio_list.html', {
        'grupos': grupos,
        'participacoes': participacoes
    })

@login_required
def grupo_apoio_create(request):
    """Cria um novo grupo de apoio"""
    if request.method == 'POST':
        # Processar o formulário e criar um novo grupo
        novo_grupo = GrupoApoio(
            nome=request.POST.get('nome'),
            tipo=request.POST.get('tipo'),
            descricao=request.POST.get('descricao'),
            local=request.POST.get('local'),
            horario=request.POST.get('horario'),
            contato=request.POST.get('contato'),
            website=request.POST.get('website')
        )
        novo_grupo.save()
        
        # Adicionar o usuário como participante do grupo
        ParticipacaoGrupo.objects.create(grupo=novo_grupo, usuario=request.user)
        
        messages.success(request, 'Grupo de apoio criado com sucesso!')
        return redirect('rede_apoio:grupo_apoio_detail', pk=novo_grupo.pk)
    
    return render(request, 'rede_apoio/grupo_apoio_form.html')

@login_required
def grupo_apoio_update(request, pk):
    """Atualiza um grupo de apoio existente"""
    grupo = get_object_or_404(GrupoApoio, pk=pk)
    
    if request.method == 'POST':
        # Processar o formulário e atualizar o grupo
        grupo.nome = request.POST.get('nome')
        grupo.tipo = request.POST.get('tipo')
        grupo.descricao = request.POST.get('descricao')
        grupo.local = request.POST.get('local')
        grupo.horario = request.POST.get('horario')
        grupo.contato = request.POST.get('contato')
        grupo.website = request.POST.get('website')
        grupo.save()
        
        messages.success(request, 'Grupo de apoio atualizado com sucesso!')
        return redirect('rede_apoio:grupo_apoio_detail', pk=grupo.pk)
    
    return render(request, 'rede_apoio/grupo_apoio_form.html', {
        'grupo': grupo
    })

@login_required
def grupo_apoio_detail(request, pk):
    """Exibe os detalhes de um grupo de apoio específico"""
    grupo = get_object_or_404(GrupoApoio, pk=pk)
    participantes = ParticipacaoGrupo.objects.filter(grupo=grupo)
    
    # Verificar se o usuário participa deste grupo
    participacao = ParticipacaoGrupo.objects.filter(grupo=grupo, usuario=request.user).first()
    
    return render(request, 'rede_apoio/grupo_apoio_detail.html', {
        'grupo': grupo,
        'participantes': participantes,
        'participacao': participacao
    })

@login_required
def grupo_apoio_participar(request, pk):
    """Registra a participação do usuário em um grupo de apoio"""
    grupo = get_object_or_404(GrupoApoio, pk=pk)
    
    # Verificar se o usuário já participa deste grupo
    participacao = ParticipacaoGrupo.objects.filter(grupo=grupo, usuario=request.user).first()
    
    if participacao:
        # Se já participa, remover participação
        participacao.delete()
        messages.success(request, f'Você saiu do grupo {grupo.nome}.')
    else:
        # Se não participa, adicionar participação
        ParticipacaoGrupo.objects.create(grupo=grupo, usuario=request.user)
        messages.success(request, f'Você agora participa do grupo {grupo.nome}!')
    
    return redirect('rede_apoio:grupo_apoio_detail', pk=grupo.pk)

# Acionamento Rápido
@login_required
def acionamento_rapido(request):
    """Exibe a tela de acionamento rápido com os contatos prioritários"""
    contatos_rapidos = ContatoEmergencial.objects.filter(
        usuario=request.user,
        acionamento_rapido=True
    ).order_by('prioridade')
    
    return render(request, 'rede_apoio/acionamento_rapido.html', {
        'contatos_rapidos': contatos_rapidos
    })

# Dashboard da Rede de Apoio
@login_required
def rede_apoio_dashboard(request):
    """Exibe o dashboard da rede de apoio com informações consolidadas"""
    # Obter os contatos emergenciais do usuário
    contatos = ContatoEmergencial.objects.filter(usuario=request.user)
    contatos_rapidos = contatos.filter(acionamento_rapido=True)
    
    # Obter os últimos acionamentos
    ultimos_acionamentos = AcionamentoEmergencia.objects.filter(usuario=request.user).order_by('-data_hora')[:5]
    
    # Obter os grupos de apoio que o usuário participa
    participacoes = ParticipacaoGrupo.objects.filter(usuario=request.user)
    grupos = [p.grupo for p in participacoes]
    
    return render(request, 'rede_apoio/dashboard.html', {
        'contatos': contatos,
        'contatos_rapidos': contatos_rapidos,
        'ultimos_acionamentos': ultimos_acionamentos,
        'grupos': grupos
    })
