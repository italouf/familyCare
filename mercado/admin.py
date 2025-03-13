from django.contrib import admin
from django.utils.html import format_html
from .models import Produto, PromocaoProduto, Compra, ItemCompra

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'preco', 'estoque', 'destaque', 'display_imagem')
    list_filter = ('categoria', 'destaque')
    search_fields = ('nome', 'descricao')
    list_editable = ('preco', 'estoque', 'destaque')
    readonly_fields = ('display_imagem_detail',)
    
    def display_imagem(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;"/>', obj.imagem.url)
        return "-"
    display_imagem.short_description = 'Imagem'
    
    def display_imagem_detail(self, obj):
        if obj.imagem:
            return format_html('<img src="{}" width="300" style="max-height: 300px; object-fit: contain;"/>', obj.imagem.url)
        return "-"
    display_imagem_detail.short_description = 'Visualização da Imagem'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'categoria')
        }),
        ('Preço e Estoque', {
            'fields': ('preco', 'estoque')
        }),
        ('Imagem', {
            'fields': ('imagem', 'display_imagem_detail')
        }),
        ('Configurações', {
            'fields': ('destaque',)
        })
    )

@admin.register(PromocaoProduto)
class PromocaoProdutoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'produto', 'desconto', 'data_inicio', 'data_fim', 'esta_ativa')
    list_filter = ('data_inicio', 'data_fim')
    search_fields = ('titulo', 'produto__nome')

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data', 'total', 'status')
    list_filter = ('status', 'data')
    search_fields = ('usuario__username',)

@admin.register(ItemCompra)
class ItemCompraAdmin(admin.ModelAdmin):
    list_display = ('compra', 'produto', 'quantidade', 'preco_unitario', 'subtotal')
    list_filter = ('compra__status',)
    search_fields = ('produto__nome', 'compra__usuario__username')
