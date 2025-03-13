from educacional.models import Ebook
from django.core.files import File
from decimal import Decimal
import os
from django.utils import timezone

# Verificar se já existem ebooks no banco de dados
if Ebook.objects.count() > 0:
    print(f"Já existem {Ebook.objects.count()} e-books no banco de dados. Pulando criação.")
else:
    # Criar e-books de Saúde
    ebook1 = Ebook(
        titulo="O Poder do Hábito",
        autor="Charles Duhigg",
        descricao="Por que fazemos o que fazemos na vida e nos negócios. Este livro explora como os hábitos funcionam e como podemos transformá-los para melhorar nossa saúde e bem-estar.",
        categoria="Saúde",
        paginas=408,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('49.90'),
        url="https://www.amazon.com.br/poder-do-hábito-Charles-Duhigg/dp/8539004119"
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/cursos/primeiros-socorros.jpg'):
        with open('media/cursos/primeiros-socorros.jpg', 'rb') as img_file:
            ebook1.capa.save('poder-do-habito.jpg', File(img_file), save=False)
    
    ebook1.save()
    print(f"E-book criado: {ebook1}")
    
    ebook2 = Ebook(
        titulo="Mente Inquieta: Estratégias para Crianças com TDAH, Ansiedade e Autismo",
        autor="Dawn Huebner",
        descricao="Um guia prático para pais e cuidadores sobre como ajudar crianças com desafios de saúde mental, oferecendo estratégias baseadas em evidências para apoiar seu desenvolvimento emocional.",
        categoria="Saúde",
        paginas=224,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('39.90'),
        url="https://www.amazon.com.br/Mente-Inquieta-Estratégias-Crianças-Ansiedade/dp/6555353023"
    )
    
    if os.path.exists('media/cursos/saude-mental.jpg'):
        with open('media/cursos/saude-mental.jpg', 'rb') as img_file:
            ebook2.capa.save('mente-inquieta.jpg', File(img_file), save=False)
    
    ebook2.save()
    print(f"E-book criado: {ebook2}")
    
    ebook3 = Ebook(
        titulo="Como Envelhecer Sem Ficar Velho",
        autor="Mirian Goldenberg",
        descricao="Um guia sobre como envelhecer com saúde e qualidade de vida, abordando aspectos físicos, emocionais e sociais do envelhecimento saudável.",
        categoria="Saúde",
        paginas=224,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('34.90'),
        url="https://www.amazon.com.br/Como-envelhecer-sem-ficar-velho/dp/6555111224"
    )
    
    if os.path.exists('media/cursos/doencas-cronicas.jpg'):
        with open('media/cursos/doencas-cronicas.jpg', 'rb') as img_file:
            ebook3.capa.save('envelhecer-sem-ficar-velho.jpg', File(img_file), save=False)
    
    ebook3.save()
    print(f"E-book criado: {ebook3}")
    
    # Criar e-books de Nutrição
    ebook4 = Ebook(
        titulo="Comer, Rezar, Amar",
        autor="Elizabeth Gilbert",
        descricao="Uma jornada de autodescoberta através da comida, espiritualidade e relacionamentos, que inspirou milhões de pessoas a repensarem suas escolhas alimentares e estilo de vida.",
        categoria="Nutrição",
        paginas=368,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('42.90'),
        url="https://www.amazon.com.br/Comer-rezar-amar-Elizabeth-Gilbert/dp/8528614522"
    )
    
    if os.path.exists('media/cursos/nutricao-saudadevel.jpg'):
        with open('media/cursos/nutricao-saudadevel.jpg', 'rb') as img_file:
            ebook4.capa.save('comer-rezar-amar.jpg', File(img_file), save=False)
    
    ebook4.save()
    print(f"E-book criado: {ebook4}")
    
    ebook5 = Ebook(
        titulo="Dieta Flexível & Nutrição",
        autor="Caio Bottura",
        descricao="Um guia completo sobre nutrição esportiva e dieta flexível, explicando como equilibrar macronutrientes para atingir objetivos de saúde e performance física para toda a família.",
        categoria="Nutrição",
        paginas=256,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('59.90'),
        url="https://www.amazon.com.br/Dieta-Flexível-Nutrição-Caio-Bottura/dp/8568905072"
    )
    
    if os.path.exists('media/cursos/nutricao-esportiva-familiar.jpg'):
        with open('media/cursos/nutricao-esportiva-familiar.jpg', 'rb') as img_file:
            ebook5.capa.save('dieta-flexivel-nutricao.jpg', File(img_file), save=False)
    
    ebook5.save()
    print(f"E-book criado: {ebook5}")
    
    # Criar e-books de Bem Estar
    ebook6 = Ebook(
        titulo="Mindfulness: Atenção Plena",
        autor="Mark Williams e Danny Penman",
        descricao="Um programa de oito semanas para reduzir a ansiedade, o estresse e a depressão, com técnicas de meditação e mindfulness adaptadas para o contexto familiar.",
        categoria="Bem Estar",
        paginas=256,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('45.90'),
        url="https://www.amazon.com.br/Mindfulness-atenção-plena-Mark-Williams/dp/8539004070"
    )
    
    if os.path.exists('media/cursos/meditacao-familia.jpg'):
        with open('media/cursos/meditacao-familia.jpg', 'rb') as img_file:
            ebook6.capa.save('mindfulness-atencao-plena.jpg', File(img_file), save=False)
    
    ebook6.save()
    print(f"E-book criado: {ebook6}")
    
    ebook7 = Ebook(
        titulo="Luz nas Yoga Sutras de Patanjali",
        autor="B.K.S. Iyengar",
        descricao="Uma obra clássica sobre os fundamentos filosóficos e práticos do yoga, com orientações para praticantes de todas as idades e níveis de experiência.",
        categoria="Bem Estar",
        paginas=384,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('69.90'),
        url="https://www.amazon.com.br/Luz-nos-Yoga-Sutras-Patanjali/dp/8531516455"
    )
    
    if os.path.exists('media/cursos/ioga-todas-idades.jpg'):
        with open('media/cursos/ioga-todas-idades.jpg', 'rb') as img_file:
            ebook7.capa.save('luz-yoga-sutras-patanjali.jpg', File(img_file), save=False)
    
    ebook7.save()
    print(f"E-book criado: {ebook7}")
    
    # Criar e-books de Tecnologia
    ebook8 = Ebook(
        titulo="Criando Filhos na Era Digital",
        autor="Jordan Shapiro",
        descricao="Um guia essencial para pais sobre como criar filhos em um mundo dominado pela tecnologia, abordando temas como segurança online, tempo de tela e desenvolvimento saudável.",
        categoria="Tecnologia",
        paginas=320,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('49.90'),
        url="https://www.amazon.com.br/Criando-filhos-digital-Jordan-Shapiro/dp/8551005936"
    )
    
    if os.path.exists('media/cursos/seguranca-digital-familia.jpg'):
        with open('media/cursos/seguranca-digital-familia.jpg', 'rb') as img_file:
            ebook8.capa.save('criando-filhos-era-digital.jpg', File(img_file), save=False)
    
    ebook8.save()
    print(f"E-book criado: {ebook8}")
    
    ebook9 = Ebook(
        titulo="Tecnologia Assistiva: Recursos e Metodologia",
        autor="Teófilo Galvão Filho",
        descricao="Um livro sobre tecnologias assistivas para pessoas com deficiência, abordando recursos, metodologias e aplicações práticas para promover a inclusão e acessibilidade.",
        categoria="Tecnologia",
        paginas=228,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('65.00'),
        url="https://www.amazon.com.br/Tecnologia-Assistiva-Recursos-Metodologia-Teófilo/dp/8578611365"
    )
    
    if os.path.exists('media/cursos/tecnologia_assistiva.jpg'):
        with open('media/cursos/tecnologia_assistiva.jpg', 'rb') as img_file:
            ebook9.capa.save('tecnologia-assistiva-recursos.jpg', File(img_file), save=False)
    
    ebook9.save()
    print(f"E-book criado: {ebook9}")
    
    # Criar e-books de Terapias Alternativas
    ebook10 = Ebook(
        titulo="Medicina Tradicional Chinesa",
        autor="Giovanni Maciocia",
        descricao="Uma obra de referência sobre os fundamentos da medicina tradicional chinesa, incluindo acupuntura, fitoterapia e práticas de bem-estar que podem ser integradas ao cuidado familiar.",
        categoria="Terapias Alternativas",
        paginas=1016,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('299.90'),
        url="https://www.amazon.com.br/Fundamentos-Medicina-Tradicional-Chinesa-Giovanni/dp/8527714116"
    )
    
    if os.path.exists('media/cursos/terapias-integrativas.jpg'):
        with open('media/cursos/terapias-integrativas.jpg', 'rb') as img_file:
            ebook10.capa.save('medicina-tradicional-chinesa.jpg', File(img_file), save=False)
    
    ebook10.save()
    print(f"E-book criado: {ebook10}")
    
    print("Criação de e-books concluída com sucesso!")