from nutricao.models import Marmita
from django.core.files import File
from decimal import Decimal
import os

# Verificar se já existem marmitas no banco de dados
if Marmita.objects.count() > 0:
    print(f"Já existem {Marmita.objects.count()} marmitas no banco de dados. Pulando criação.")
else:
    # Criar marmitas de café da manhã
    # Fitness
    marmita1 = Marmita(
        nome="Omelete de Claras",
        descricao="Omelete preparado com claras de ovos, espinafre, tomate e queijo cottage. Rico em proteínas e baixo em gorduras.",
        categoria="fitness",
        tipo_refeicao="cafe_manha",
        calorias=220,
        proteinas=Decimal('18.5'),
        carboidratos=Decimal('6.2'),
        gorduras=Decimal('3.8'),
        preco=Decimal('15.90'),
        disponivel=True
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/marmitas/fitness_cafe_manha.jpg'):
        with open('media/marmitas/fitness_cafe_manha.jpg', 'rb') as img_file:
            marmita1.imagem.save('fitness_cafe_manha.jpg', File(img_file), save=False)
    
    marmita1.save()
    print(f"Marmita criada: {marmita1}")
    
    # Vegetariana
    marmita2 = Marmita(
        nome="Iogurte com Granola",
        descricao="Iogurte natural com granola caseira, frutas vermelhas e mel. Opção vegetariana rica em probióticos.",
        categoria="vegetariana",
        tipo_refeicao="cafe_manha",
        calorias=280,
        proteinas=Decimal('12.0'),
        carboidratos=Decimal('42.5'),
        gorduras=Decimal('6.3'),
        preco=Decimal('14.50'),
        disponivel=True
    )
    marmita2.save()
    print(f"Marmita criada: {marmita2}")
    
    # Geral
    marmita3 = Marmita(
        nome="Sanduíche Integral",
        descricao="Sanduíche de pão integral com peito de peru, queijo branco, alface e tomate. Opção balanceada para o café da manhã.",
        categoria="geral",
        tipo_refeicao="cafe_manha",
        calorias=320,
        proteinas=Decimal('15.8'),
        carboidratos=Decimal('38.2'),
        gorduras=Decimal('9.5'),
        preco=Decimal('16.90'),
        disponivel=True
    )
    marmita3.save()
    print(f"Marmita criada: {marmita3}")
    
    # Criar marmitas de almoço
    # Fitness
    marmita4 = Marmita(
        nome="Frango Grelhado com Legumes",
        descricao="Peito de frango grelhado com mix de legumes no vapor e arroz integral. Rico em proteínas e fibras.",
        categoria="fitness",
        tipo_refeicao="almoco",
        calorias=420,
        proteinas=Decimal('32.5'),
        carboidratos=Decimal('45.0'),
        gorduras=Decimal('8.2'),
        preco=Decimal('22.90'),
        disponivel=True
    )
    marmita4.save()
    print(f"Marmita criada: {marmita4}")
    
    # Vegetariana
    marmita5 = Marmita(
        nome="Bowl de Quinoa",
        descricao="Bowl de quinoa com grão-de-bico, abacate, tomate cereja e molho de iogurte. Opção vegetariana completa.",
        categoria="vegetariana",
        tipo_refeicao="almoco",
        calorias=380,
        proteinas=Decimal('14.2'),
        carboidratos=Decimal('52.6'),
        gorduras=Decimal('12.8'),
        preco=Decimal('24.50'),
        disponivel=True
    )
    marmita5.save()
    print(f"Marmita criada: {marmita5}")
    
    # Geral
    marmita6 = Marmita(
        nome="Escondidinho de Carne",
        descricao="Escondidinho de carne moída com purê de batata doce. Opção saborosa e nutritiva.",
        categoria="geral",
        tipo_refeicao="almoco",
        calorias=520,
        proteinas=Decimal('28.5'),
        carboidratos=Decimal('58.3'),
        gorduras=Decimal('18.2'),
        preco=Decimal('25.90'),
        disponivel=True
    )
    marmita6.save()
    print(f"Marmita criada: {marmita6}")
    
    # Criar marmitas de jantar
    # Fitness
    marmita7 = Marmita(
        nome="Salmão com Aspargos",
        descricao="Filé de salmão grelhado com aspargos e purê de couve-flor. Rico em ômega-3 e proteínas de alta qualidade.",
        categoria="fitness",
        tipo_refeicao="jantar",
        calorias=380,
        proteinas=Decimal('29.8'),
        carboidratos=Decimal('12.5'),
        gorduras=Decimal('22.3'),
        preco=Decimal('32.90'),
        disponivel=True
    )
    marmita7.save()
    print(f"Marmita criada: {marmita7}")
    
    # Vegetariana
    marmita8 = Marmita(
        nome="Risoto de Cogumelos",
        descricao="Risoto de cogumelos variados com ervas frescas e queijo parmesão. Opção vegetariana reconfortante.",
        categoria="vegetariana",
        tipo_refeicao="jantar",
        calorias=420,
        proteinas=Decimal('10.2'),
        carboidratos=Decimal('65.8'),
        gorduras=Decimal('14.5'),
        preco=Decimal('28.50'),
        disponivel=True
    )
    marmita8.save()
    print(f"Marmita criada: {marmita8}")
    
    # Geral
    marmita9 = Marmita(
        nome="Strogonoff de Frango",
        descricao="Strogonoff de frango com arroz integral e batata palha assada. Versão mais leve do prato tradicional.",
        categoria="geral",
        tipo_refeicao="jantar",
        calorias=480,
        proteinas=Decimal('26.5'),
        carboidratos=Decimal('52.3'),
        gorduras=Decimal('16.8'),
        preco=Decimal('26.90'),
        disponivel=True
    )
    marmita9.save()
    print(f"Marmita criada: {marmita9}")
    
    # Criar marmitas de lanche
    # Fitness
    marmita10 = Marmita(
        nome="Mix de Castanhas",
        descricao="Mix de castanhas, amêndoas e nozes com frutas desidratadas. Lanche rico em gorduras boas e antioxidantes.",
        categoria="fitness",
        tipo_refeicao="lanche",
        calorias=280,
        proteinas=Decimal('8.5'),
        carboidratos=Decimal('14.2'),
        gorduras=Decimal('22.6'),
        preco=Decimal('18.90'),
        disponivel=True
    )
    marmita10.save()
    print(f"Marmita criada: {marmita10}")
    
    # Vegetariana
    marmita11 = Marmita(
        nome="Wrap de Hummus",
        descricao="Wrap integral com hummus, legumes grelhados e folhas verdes. Lanche vegetariano completo.",
        categoria="vegetariana",
        tipo_refeicao="lanche",
        calorias=320,
        proteinas=Decimal('9.8'),
        carboidratos=Decimal('42.5'),
        gorduras=Decimal('12.3'),
        preco=Decimal('19.50'),
        disponivel=True
    )
    marmita11.save()
    print(f"Marmita criada: {marmita11}")
    
    # Geral
    marmita12 = Marmita(
        nome="Muffin Proteico",
        descricao="Muffin de banana com whey protein e gotas de chocolate. Lanche doce e proteico.",
        categoria="geral",
        tipo_refeicao="lanche",
        calorias=250,
        proteinas=Decimal('15.2'),
        carboidratos=Decimal('28.5'),
        gorduras=Decimal('8.3'),
        preco=Decimal('12.90'),
        disponivel=True
    )
    marmita12.save()
    print(f"Marmita criada: {marmita12}")
    
    # Criar marmitas de sobremesa
    # Fitness
    marmita13 = Marmita(
        nome="Pudim de Chia",
        descricao="Pudim de chia com leite de amêndoas e frutas vermelhas. Sobremesa rica em fibras e ômega-3.",
        categoria="fitness",
        tipo_refeicao="sobremesa",
        calorias=180,
        proteinas=Decimal('6.2'),
        carboidratos=Decimal('22.5'),
        gorduras=Decimal('8.8'),
        preco=Decimal('15.90'),
        disponivel=True
    )
    marmita13.save()
    print(f"Marmita criada: {marmita13}")
    
    # Vegetariana
    marmita14 = Marmita(
        nome="Mousse de Abacate",
        descricao="Mousse de abacate com cacau e toque de mel. Sobremesa vegetariana cremosa e nutritiva.",
        categoria="vegetariana",
        tipo_refeicao="sobremesa",
        calorias=220,
        proteinas=Decimal('3.5'),
        carboidratos=Decimal('18.2'),
        gorduras=Decimal('16.5'),
        preco=Decimal('16.50'),
        disponivel=True
    )
    marmita14.save()
    print(f"Marmita criada: {marmita14}")
    
    # Geral
    marmita15 = Marmita(
        nome="Brownie Fit",
        descricao="Brownie de chocolate meio amargo com farinha de amêndoas. Versão mais saudável da sobremesa clássica.",
        categoria="geral",
        tipo_refeicao="sobremesa",
        calorias=250,
        proteinas=Decimal('5.8'),
        carboidratos=Decimal('24.3'),
        gorduras=Decimal('15.2'),
        preco=Decimal('14.90'),
        disponivel=True
    )
    marmita15.save()
    print(f"Marmita criada: {marmita15}")
    
    print(f"\nTotal de marmitas criadas: {Marmita.objects.count()}")
    print("Marmitas por categoria:")
    print(f"- Fitness: {Marmita.objects.filter(categoria='fitness').count()}")
    print(f"- Vegetariana: {Marmita.objects.filter(categoria='vegetariana').count()}")
    print(f"- Geral: {Marmita.objects.filter(categoria='geral').count()}")
    
    print("\nMarmitas por tipo de refeição:")
    print(f"- Café da manhã: {Marmita.objects.filter(tipo_refeicao='cafe_manha').count()}")
    print(f"- Almoço: {Marmita.objects.filter(tipo_refeicao='almoco').count()}")
    print(f"- Jantar: {Marmita.objects.filter(tipo_refeicao='jantar').count()}")
    print(f"- Lanche: {Marmita.objects.filter(tipo_refeicao='lanche').count()}")
    print(f"- Sobremesa: {Marmita.objects.filter(tipo_refeicao='sobremesa').count()}")

print("\nPara usar este script no shell do Django, execute o seguinte comando:")
print("exec(open('create_marmitas.py').read())")