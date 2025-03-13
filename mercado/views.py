from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Produto, PromocaoProduto
from educacional.models import ListaCompras, ItemListaCompras

# View para listar todos os produtos
class ProdutoListView(ListView):
    model = Produto
    template_name = 'mercado/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = dict(Produto.CATEGORIA_CHOICES)
        context['promocoes'] = PromocaoProduto.objects.filter(data_inicio__lte=timezone.now().date(), data_fim__gte=timezone.now().date())[:6]
        context['destaques'] = Produto.objects.filter(destaque=True)[:6]
        return context

# View para detalhar um produto específico
class ProdutoDetailView(DetailView):
    model = Produto
    template_name = 'mercado/produto_detail.html'
    context_object_name = 'produto'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto = self.get_object()
        context['promocao'] = PromocaoProduto.objects.filter(
            produto=produto,
            data_inicio__lte=timezone.now().date(),
            data_fim__gte=timezone.now().date()
        ).first()
        
        # Produtos relacionados da mesma categoria
        context['produtos_relacionados'] = Produto.objects.filter(
            categoria=produto.categoria
        ).exclude(id=produto.id)[:4]
        
        # Se o usuário estiver logado, buscar suas listas de compras
        if self.request.user.is_authenticated:
            context['listas_compras'] = ListaCompras.objects.filter(
                usuario=self.request.user,
                concluida=False
            )
        
        return context

# View para listar produtos por categoria
class ProdutoCategoriaListView(ListView):
    model = Produto
    template_name = 'mercado/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        return Produto.objects.filter(categoria=self.kwargs['categoria'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = dict(Produto.CATEGORIA_CHOICES)
        context['categoria_atual'] = self.kwargs['categoria']
        context['categoria_nome'] = dict(Produto.CATEGORIA_CHOICES).get(self.kwargs['categoria'])
        return context

# View para listar promoções ativas
class PromocaoListView(ListView):
    template_name = 'mercado/promocao_list.html'
    context_object_name = 'promocoes'
    paginate_by = 12
    
    def get_queryset(self):
        return PromocaoProduto.objects.filter(
            data_inicio__lte=timezone.now().date(),
            data_fim__gte=timezone.now().date()
        )

# View para buscar produtos
class ProdutoBuscaView(ListView):
    model = Produto
    template_name = 'mercado/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Produto.objects.filter(
                Q(nome__icontains=query) | 
                Q(descricao__icontains=query) |
                Q(categoria__icontains=query)
            )
        return Produto.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

def home(request):
    promocoes = PromocaoProduto.objects.filter(
        data_inicio__lte=timezone.now().date(),
        data_fim__gte=timezone.now().date()
    )[:6]
    return render(request, 'home.html', {'promocoes': promocoes})
# View para adicionar produto à lista de compras
@login_required
def adicionar_produto_lista(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        lista_id = request.POST.get('lista_id')
        quantidade = int(request.POST.get('quantidade', 1))
        
        # Se não foi selecionada uma lista, criar uma nova
        if not lista_id:
            lista = ListaCompras.objects.create(
                usuario=request.user,
                nome=f"Lista de {request.user.username} - {timezone.now().strftime('%d/%m/%Y')}"
            )
        else:
            lista = get_object_or_404(ListaCompras, id=lista_id, usuario=request.user)
        
        # Verificar se o produto já está na lista
        item_existente = ItemListaCompras.objects.filter(lista=lista, nome=produto.nome).first()
        
        if item_existente:
            item_existente.quantidade += quantidade
            item_existente.save()
            messages.success(request, f'Quantidade de {produto.nome} atualizada na lista {lista.nome}!')
        else:
            # Adicionar o produto à lista
            ItemListaCompras.objects.create(
                lista=lista,
                nome=produto.nome,
                quantidade=quantidade,
                observacao=f"Produto ID: {produto.id} - Preço: R$ {produto.preco}"
            )
            messages.success(request, f'{produto.nome} adicionado à lista {lista.nome}!')
        
        return redirect('mercado:produto_detail', pk=produto.id)
    
    return redirect('mercado:produto_list')

# View para remover produto da lista de compras
@login_required
def remover_produto_lista(request, produto_id):
    if request.method == 'POST':
        lista_id = request.POST.get('lista_id')
        item_id = request.POST.get('item_id')
        
        if lista_id and item_id:
            lista = get_object_or_404(ListaCompras, id=lista_id, usuario=request.user)
            item = get_object_or_404(ItemListaCompras, id=item_id, lista=lista)
            produto_nome = item.nome
            item.delete()
            messages.success(request, f'{produto_nome} removido da lista {lista.nome}!')
    
    return redirect('mercado:produto_detail', pk=produto_id)
