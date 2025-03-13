from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .models import Curso, InscricaoCurso, Ebook, Videoaula, Midia, ListaCompras, ItemListaCompras, Evento
from random import sample

def get_random_courses():
    """Retorna uma seleção aleatória de cursos para exibição na homepage"""
    all_courses = list(Curso.objects.all())
    num_courses = min(len(all_courses), 4)  # Limita a 4 cursos
    if num_courses > 0:
        return sample(all_courses, num_courses)
    return []

# Views para Cursos
@login_required
def curso_list(request):
    """Lista todos os cursos disponíveis"""
    categoria = request.GET.get('categoria', '')
    nivel = request.GET.get('nivel', '')
    
    cursos = Curso.objects.all()
    
    if categoria:
        cursos = cursos.filter(categoria=categoria)
    if nivel:
        cursos = cursos.filter(nivel=nivel)
    
    # Verificar em quais cursos o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).values_list('curso_id', flat=True)
    
    return render(request, 'educacional/curso_list.html', {
        'cursos': cursos,
        'categoria_selecionada': categoria,
        'nivel_selecionado': nivel,
        'categorias': dict(Curso.CATEGORIA_CHOICES),
        'niveis': dict(Curso.NIVEL_CHOICES),
        'inscricoes': inscricoes
    })

# Lista de Compras
@login_required
def lista_compras_list(request):
    """Exibe a lista de compras do usuário"""
    # Obter as listas de compras do usuário
    listas = ListaCompras.objects.filter(usuario=request.user).order_by('-data_atualizacao')
    
    return render(request, 'educacional/lista_compras_list.html', {
        'listas': listas
    })

@login_required
def lista_compras_create(request):
    """Cria uma nova lista de compras"""
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            lista = ListaCompras.objects.create(
                usuario=request.user,
                nome=nome
            )
            
            # Processar os itens da lista
            items_data = {}
            for key, value in request.POST.items():
                if key.startswith('items['):
                    # Extrair o índice e o campo do nome do parâmetro
                    # Formato: items[0][nome], items[0][quantidade], etc.
                    parts = key.split('][')
                    index = parts[0].split('[')[1]
                    field = parts[1].split(']')[0]
                    
                    # Inicializar o dicionário para este índice se não existir
                    if index not in items_data:
                        items_data[index] = {}
                    
                    # Adicionar o valor ao dicionário
                    items_data[index][field] = value
            
            # Criar os itens da lista de compras
            for item_data in items_data.values():
                if item_data.get('nome'):
                    ItemListaCompras.objects.create(
                        lista=lista,
                        nome=item_data.get('nome'),
                        quantidade=item_data.get('quantidade', 1),
                        unidade=item_data.get('unidade', ''),
                        observacao=item_data.get('observacao', '')
                    )
            
            messages.success(request, f'Lista de compras "{nome}" criada com sucesso!')
            return redirect('educacional:lista_compras_detail', pk=lista.pk)
    return render(request, 'educacional/lista_compras_form.html')

@login_required
def lista_compras_detail(request, pk):
    """Exibe os detalhes de uma lista de compras"""
    lista = get_object_or_404(ListaCompras, pk=pk, usuario=request.user)
    return render(request, 'educacional/lista_compras_detail.html', {
        'lista': lista
    })

@login_required
def lista_compras_edit(request, pk):
    """Edita uma lista de compras existente"""
    lista = get_object_or_404(ListaCompras, pk=pk, usuario=request.user)
    if request.method == 'POST':
        nome = request.POST.get('nome')
        if nome:
            lista.nome = nome
            lista.save()
            
            # Processar os itens da lista
            items_data = {}
            for key, value in request.POST.items():
                if key.startswith('items['):
                    # Extrair o índice e o campo do nome do parâmetro
                    parts = key.split('][')
                    index = parts[0].split('[')[1]
                    field = parts[1].split(']')[0]
                    
                    # Inicializar o dicionário para este índice se não existir
                    if index not in items_data:
                        items_data[index] = {}
                    
                    # Adicionar o valor ao dicionário
                    items_data[index][field] = value
            
            # Remover itens existentes e adicionar os novos
            lista.itens.all().delete()
            
            # Criar os itens da lista de compras
            for item_data in items_data.values():
                if item_data.get('nome'):
                    ItemListaCompras.objects.create(
                        lista=lista,
                        nome=item_data.get('nome'),
                        quantidade=item_data.get('quantidade', 1),
                        unidade=item_data.get('unidade', ''),
                        observacao=item_data.get('observacao', '')
                    )
            
            messages.success(request, f'Lista de compras "{nome}" atualizada com sucesso!')
            return redirect('educacional:lista_compras_detail', pk=lista.pk)
    return render(request, 'educacional/lista_compras_form.html', {
        'lista': lista
    })

@login_required
def lista_compras_delete(request, pk):
    """Exclui uma lista de compras"""
    lista = get_object_or_404(ListaCompras, pk=pk, usuario=request.user)
    if request.method == 'POST':
        nome = lista.nome
        lista.delete()
        messages.success(request, f'Lista de compras "{nome}" excluída com sucesso!')
        return redirect('educacional:lista_compras_list')
    return render(request, 'educacional/lista_compras_confirm_delete.html', {
        'lista': lista
    })

# Views para Eventos
@login_required
def evento_list(request):
    """Lista todos os eventos disponíveis"""
    tipo = request.GET.get('tipo', '')
    
    eventos = Evento.objects.all().order_by('data_inicio')
    
    if tipo:
        eventos = eventos.filter(tipo=tipo)
    
    # Verificar em quais eventos o usuário está participando
    eventos_participando = Evento.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/evento_list.html', {
        'eventos': eventos,
        'eventos_participando': eventos_participando,
        'tipo_selecionado': tipo,
        'tipos': dict(Evento.TIPO_CHOICES)
    })

@login_required
def evento_detail(request, pk):
    """Exibe os detalhes de um evento específico"""
    evento = get_object_or_404(Evento, pk=pk)
    
    # Verificar se o usuário está participando deste evento
    participando = Evento.objects.filter(pk=pk, usuario=request.user).exists()
    
    return render(request, 'educacional/evento_detail.html', {
        'evento': evento,
        'participando': participando
    })

@login_required
def evento_participar(request, pk):
    """Adiciona o usuário como participante de um evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    # Verificar se o usuário já está participando
    if Evento.objects.filter(pk=pk, usuario=request.user).exists():
        messages.warning(request, f'Você já está participando do evento {evento.titulo}.')
    else:
        # Criar uma cópia do evento para o usuário
        novo_evento = Evento(
            usuario=request.user,
            titulo=evento.titulo,
            descricao=evento.descricao,
            tipo=evento.tipo,
            data_inicio=evento.data_inicio,
            data_fim=evento.data_fim,
            local=evento.local,
            lembrete=True,
            tempo_lembrete=30
        )
        novo_evento.save()
        
        messages.success(request, f'Você está participando do evento {evento.titulo}!')
    
    return redirect('educacional:evento_detail', pk=evento.pk)

@login_required
def evento_cancelar(request, pk):
    """Cancela a participação do usuário em um evento"""
    evento = get_object_or_404(Evento, pk=pk)
    
    # Buscar o evento do usuário
    evento_usuario = Evento.objects.filter(usuario=request.user, titulo=evento.titulo, 
                                          data_inicio=evento.data_inicio).first()
    
    if evento_usuario:
        evento_usuario.delete()
        messages.success(request, f'Sua participação no evento {evento.titulo} foi cancelada.')
    else:
        messages.warning(request, f'Você não está participando do evento {evento.titulo}.')
    
    return redirect('educacional:evento_list')
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    
    # Registrar a visualização
    videoaula.visualizacoes += 1
    videoaula.save()
    
    return render(request, 'educacional/videoaula_assistir.html', {
        'videoaula': videoaula
    })

# Views para Catálogo de Mídias
@login_required
def midia_list(request):
    """Lista todas as mídias disponíveis no catálogo"""
    tipo = request.GET.get('tipo', '')
    
    midias = Midia.objects.all()
    
    if tipo:
        midias = midias.filter(tipo=tipo)
    
    return render(request, 'educacional/midia_list.html', {
        'midias': midias,
        'tipo_selecionado': tipo,
        'tipos': dict(Midia.TIPO_CHOICES)
    })

@login_required
def midia_detail(request, pk):
    """Exibe os detalhes de uma mídia específica"""
    midia = get_object_or_404(Midia, pk=pk)
    return render(request, 'educacional/midia_detail.html', {
        'midia': midia
    })

# Views para Progresso Educacional
@login_required
def progresso_educacional(request):
    """Exibe o progresso educacional do usuário"""
    # Obter as inscrições do usuário
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user)
    
    return render(request, 'educacional/progresso_educacional.html', {
        'inscricoes': inscricoes
    })

# Dashboard Educacional
@login_required
def educacional_dashboard(request):
    """Exibe o dashboard educacional com informações consolidadas"""
    # Obter os cursos em que o usuário está inscrito
    inscricoes = InscricaoCurso.objects.filter(usuario=request.user).order_by('-data_inscricao')[:5]
    
    # Obter os e-books mais recentes
    ebooks_recentes = Ebook.objects.all().order_by('-data_publicacao')[:3]
    
    # Obter as videoaulas mais populares
    videoaulas_populares = Videoaula.objects.all().order_by('-visualizacoes')[:3]
    
    return render(request, 'educacional/dashboard.html', {
        'inscricoes': inscricoes,
        'ebooks_recentes': ebooks_recentes,
        'videoaulas_populares': videoaulas_populares
    })

@login_required
def curso_detail(request, pk):
    """Exibe os detalhes de um curso específico"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário está inscrito neste curso
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    # Obter o progresso do usuário neste curso
    progresso = None
    
    return render(request, 'educacional/curso_detail.html', {
        'curso': curso,
        'inscricao': inscricao,
        'progresso': progresso
    })

@login_required
def curso_inscrever(request, pk):
    """Inscreve o usuário em um curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    # Verificar se o usuário já está inscrito
    inscricao = InscricaoCurso.objects.filter(curso=curso, usuario=request.user).first()
    
    if inscricao:
        messages.warning(request, f'Você já está inscrito no curso {curso.titulo}.')
    else:
        # Criar a inscrição
        InscricaoCurso.objects.create(
            curso=curso,
            usuario=request.user,
            data_inscricao=timezone.now()
        )
        
        messages.success(request, f'Inscrição no curso {curso.titulo} realizada com sucesso!')
    
    return redirect('educacional:curso_detail', pk=curso.pk)

# Views para E-books
@login_required
def ebook_list(request):
    """Lista todos os e-books disponíveis"""
    categoria = request.GET.get('categoria', '')
    
    ebooks = Ebook.objects.all()
    
    if categoria:
        ebooks = ebooks.filter(categoria=categoria)
    
    # Get unique categories from existing ebooks
    categorias = {}
    for ebook in Ebook.objects.values('categoria').distinct():
        categorias[ebook['categoria']] = ebook['categoria']
    
    return render(request, 'educacional/ebook_list.html', {
        'ebooks': ebooks,
        'categoria_selecionada': categoria,
        'categorias': categorias
    })

@login_required
def ebook_detail(request, pk):
    """Exibe os detalhes de um e-book específico"""
    ebook = get_object_or_404(Ebook, pk=pk)
    return render(request, 'educacional/ebook_detail.html', {
        'ebook': ebook
    })

@login_required
def ebook_download(request, pk):
    """Realiza o download de um e-book"""
    ebook = get_object_or_404(Ebook, pk=pk)
    
    # Registrar o download
    ebook.downloads += 1
    ebook.save()
    
    # Aqui seria implementado o código para servir o arquivo
    # Por enquanto, apenas redirecionamos para a página de detalhes
    messages.success(request, f'Download do e-book {ebook.titulo} iniciado!')
    return redirect('educacional:ebook_detail', pk=ebook.pk)

# Views para Videoaulas
@login_required
def videoaula_list(request):
    """Lista todas as videoaulas disponíveis"""
    curso_id = request.GET.get('curso', '')
    
    videoaulas = Videoaula.objects.all()
    
    if curso_id:
        videoaulas = videoaulas.filter(curso_id=curso_id)
    
    # Get all courses for filtering
    cursos = Curso.objects.all()
    
    return render(request, 'educacional/videoaula_list.html', {
        'videoaulas': videoaulas,
        'curso_selecionado': curso_id,
        'cursos': cursos
    })

@login_required
def videoaula_detail(request, pk):
    """Exibe os detalhes de uma videoaula específica"""
    videoaula = get_object_or_404(Videoaula, pk=pk)
    return render(request, 'educacional/videoaula_detail.html', {
        'videoaula': videoaula
    })

@login_required
def videoaula_assistir(request, pk):
    """Exibe a página para assistir uma videoaula"""