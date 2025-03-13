import os
import django
import sys
from datetime import datetime

# Configure Django settings
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'familyCare.settings')
django.setup()

# Import the Produto model after Django setup
from mercado.models import Produto
from django.utils import timezone

def create_produtos():
    # Check if products already exist to avoid duplicates
    if Produto.objects.count() >= 30:
        print("Já existem pelo menos 30 produtos cadastrados. Nenhum produto novo foi adicionado.")
        return
    
    # List of products to create - common supermarket products
    produtos = [
        # Alimentos básicos
        {
            'nome': 'Arroz Branco 5kg',
            'descricao': 'Arroz branco tipo 1, pacote de 5kg. Grãos selecionados de alta qualidade, livre de impurezas.',
            'categoria': 'alimentos',
            'preco': 24.90,
            'estoque': 50,
            'destaque': True
        },
        {
            'nome': 'Feijão Carioca 1kg',
            'descricao': 'Feijão carioca tipo 1, pacote de 1kg. Grãos selecionados e embalados sob rigoroso controle de qualidade.',
            'categoria': 'alimentos',
            'preco': 8.99,
            'estoque': 60,
            'destaque': True
        },
        {
            'nome': 'Açúcar Refinado 1kg',
            'descricao': 'Açúcar refinado especial, pacote de 1kg. Ideal para o preparo de bolos, doces e bebidas.',
            'categoria': 'alimentos',
            'preco': 5.49,
            'estoque': 70,
            'destaque': False
        },
        {
            'nome': 'Café Torrado e Moído 500g',
            'descricao': 'Café torrado e moído, embalagem de 500g. Blend especial com aroma intenso e sabor equilibrado.',
            'categoria': 'alimentos',
            'preco': 15.90,
            'estoque': 45,
            'destaque': True
        },
        {
            'nome': 'Óleo de Soja 900ml',
            'descricao': 'Óleo de soja refinado tipo 1, garrafa de 900ml. Rico em ômega 3 e 6, sem colesterol.',
            'categoria': 'alimentos',
            'preco': 7.99,
            'estoque': 80,
            'destaque': False
        },
        
        # Laticínios
        {
            'nome': 'Leite Integral 1L',
            'descricao': 'Leite integral UHT, embalagem Tetra Pak de 1 litro. Rico em cálcio e vitaminas A e D.',
            'categoria': 'laticinios',
            'preco': 4.99,
            'estoque': 100,
            'destaque': True
        },
        {
            'nome': 'Queijo Mussarela Fatiado 150g',
            'descricao': 'Queijo mussarela fatiado, embalagem de 150g. Ideal para sanduíches e lanches rápidos.',
            'categoria': 'laticinios',
            'preco': 12.90,
            'estoque': 30,
            'destaque': False
        },
        {
            'nome': 'Iogurte Natural 500g',
            'descricao': 'Iogurte natural integral, pote de 500g. Sem adição de açúcares, rico em probióticos.',
            'categoria': 'laticinios',
            'preco': 8.49,
            'estoque': 40,
            'destaque': False
        },
        
        # Hortifruti
        {
            'nome': 'Banana Prata (kg)',
            'descricao': 'Banana prata fresca, vendida por quilo. Fonte de potássio e vitaminas, ideal para consumo diário.',
            'categoria': 'hortifruti',
            'preco': 5.99,
            'estoque': 50,
            'destaque': True
        },
        {
            'nome': 'Maçã Gala (kg)',
            'descricao': 'Maçã gala fresca, vendida por quilo. Doce e crocante, rica em fibras e antioxidantes.',
            'categoria': 'hortifruti',
            'preco': 9.90,
            'estoque': 40,
            'destaque': False
        },
        {
            'nome': 'Tomate (kg)',
            'descricao': 'Tomate fresco para salada, vendido por quilo. Selecionado e colhido no ponto ideal de maturação.',
            'categoria': 'hortifruti',
            'preco': 6.99,
            'estoque': 35,
            'destaque': False
        },
        {
            'nome': 'Batata (kg)',
            'descricao': 'Batata inglesa fresca, vendida por quilo. Tubérculo versátil, ideal para diversos preparos culinários.',
            'categoria': 'hortifruti',
            'preco': 4.99,
            'estoque': 60,
            'destaque': False
        },
        
        # Carnes
        {
            'nome': 'Peito de Frango (kg)',
            'descricao': 'Peito de frango resfriado, vendido por quilo. Corte magro e versátil, fonte de proteínas de alta qualidade.',
            'categoria': 'carnes',
            'preco': 16.90,
            'estoque': 25,
            'destaque': True
        },
        {
            'nome': 'Carne Moída (kg)',
            'descricao': 'Carne bovina moída de primeira, vendida por quilo. Ideal para preparar hambúrgueres, molhos e recheios.',
            'categoria': 'carnes',
            'preco': 32.90,
            'estoque': 20,
            'destaque': False
        },
        {
            'nome': 'Linguiça Toscana (kg)',
            'descricao': 'Linguiça toscana suína, vendida por quilo. Temperada com especiarias selecionadas, ideal para churrasco.',
            'categoria': 'carnes',
            'preco': 22.90,
            'estoque': 15,
            'destaque': False
        },
        
        # Padaria
        {
            'nome': 'Pão Francês (kg)',
            'descricao': 'Pão francês fresco, vendido por quilo. Produzido diariamente com farinha de trigo selecionada.',
            'categoria': 'padaria',
            'preco': 13.90,
            'estoque': 30,
            'destaque': True
        },
        {
            'nome': 'Bolo de Chocolate',
            'descricao': 'Bolo de chocolate caseiro, unidade de aproximadamente 500g. Macio e com cobertura de chocolate.',
            'categoria': 'padaria',
            'preco': 18.90,
            'estoque': 10,
            'destaque': False
        },
        
        # Bebidas
        {
            'nome': 'Refrigerante Cola 2L',
            'descricao': 'Refrigerante sabor cola, garrafa pet de 2 litros. Bebida gaseificada refrescante.',
            'categoria': 'bebidas',
            'preco': 8.99,
            'estoque': 50,
            'destaque': True
        },
        {
            'nome': 'Suco de Laranja Natural 1L',
            'descricao': 'Suco de laranja 100% natural, garrafa de 1 litro. Sem adição de açúcares ou conservantes.',
            'categoria': 'bebidas',
            'preco': 12.90,
            'estoque': 20,
            'destaque': False
        },
        {
            'nome': 'Água Mineral 500ml',
            'descricao': 'Água mineral sem gás, garrafa de 500ml. Água pura e cristalina de fonte natural.',
            'categoria': 'bebidas',
            'preco': 2.49,
            'estoque': 120,
            'destaque': False
        },
        
        # Limpeza
        {
            'nome': 'Detergente Líquido 500ml',
            'descricao': 'Detergente líquido para louças, frasco de 500ml. Fórmula concentrada que remove gorduras com eficiência.',
            'categoria': 'limpeza',
            'preco': 3.49,
            'estoque': 70,
            'destaque': False
        },
        {
            'nome': 'Sabão em Pó 1kg',
            'descricao': 'Sabão em pó para roupas, embalagem de 1kg. Limpa e perfuma, removendo as manchas mais difíceis.',
            'categoria': 'limpeza',
            'preco': 12.90,
            'estoque': 45,
            'destaque': True
        },
        {
            'nome': 'Água Sanitária 2L',
            'descricao': 'Água sanitária multiuso, garrafa de 2 litros. Alveja, desinfeta e elimina germes e bactérias.',
            'categoria': 'limpeza',
            'preco': 7.99,
            'estoque': 60,
            'destaque': False
        },
        
        # Higiene Pessoal
        {
            'nome': 'Papel Higiênico 12 rolos',
            'descricao': 'Papel higiênico folha dupla, pacote com 12 rolos de 30 metros cada. Macio e resistente.',
            'categoria': 'higiene_pessoal',
            'preco': 19.90,
            'estoque': 40,
            'destaque': True
        },
        {
            'nome': 'Shampoo 350ml',
            'descricao': 'Shampoo para todos os tipos de cabelo, frasco de 350ml. Limpa profundamente e dá brilho aos fios.',
            'categoria': 'higiene_pessoal',
            'preco': 14.90,
            'estoque': 35,
            'destaque': False
        },
        {
            'nome': 'Sabonete em Barra 90g',
            'descricao': 'Sabonete em barra hidratante, unidade de 90g. Perfume suave e agradável, ideal para uso diário.',
            'categoria': 'higiene_pessoal',
            'preco': 2.99,
            'estoque': 80,
            'destaque': False
        },
        {
            'nome': 'Creme Dental 90g',
            'descricao': 'Creme dental com flúor, tubo de 90g. Protege contra cáries e fortalece o esmalte dos dentes.',
            'categoria': 'higiene_pessoal',
            'preco': 4.99,
            'estoque': 65,
            'destaque': False
        },
        
        # Congelados
        {
            'nome': 'Pizza Congelada Mussarela',
            'descricao': 'Pizza congelada sabor mussarela, unidade de 450g. Pronta em minutos, com massa crocante e queijo derretido.',
            'categoria': 'congelados',
            'preco': 16.90,
            'estoque': 25,
            'destaque': True
        },
        {
            'nome': 'Lasanha Congelada Bolonhesa',
            'descricao': 'Lasanha congelada à bolonhesa, bandeja de 600g. Camadas de massa intercaladas com molho de carne e queijo.',
            'categoria': 'congelados',
            'preco': 19.90,
            'estoque': 20,
            'destaque': False
        },
        {
            'nome': 'Batata Frita Congelada 400g',
            'descricao': 'Batata frita palito congelada, pacote de 400g. Prática e rápida de preparar, dourada e crocante.',
            'categoria': 'congelados',
            'preco': 10.90,
            'estoque': 30,
            'destaque': False
        },
    ]
    
    # Create each product
    for produto_data in produtos:
        produto = Produto(
            nome=produto_data['nome'],
            descricao=produto_data['descricao'],
            categoria=produto_data['categoria'],
            preco=produto_data['preco'],
            estoque=produto_data['estoque'],
            data_cadastro=timezone.now(),
            destaque=produto_data['destaque']
        )
        produto.save()
        print(f"Produto '{produto.nome}' criado com sucesso!")
    
    print(f"\nTotal de {len(produtos)} produtos criados!")

if __name__ == '__main__':
    print("Iniciando criação de produtos de supermercado...")
    create_produtos()
    print("Processo finalizado!")