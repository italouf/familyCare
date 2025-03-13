from educacional.models import Curso, Videoaula
from django.core.files import File
from decimal import Decimal
import os
from django.utils import timezone

# Verificar se já existem cursos no banco de dados
if Curso.objects.count() > 0:
    print(f"Já existem {Curso.objects.count()} cursos no banco de dados. Pulando criação.")
else:
    # Criar cursos de Nutrição
    # Iniciante
    curso1 = Curso(
        titulo="Fundamentos da Nutrição Saudável",
        descricao="Aprenda os princípios básicos da nutrição e como montar refeições equilibradas para toda a família. Este curso aborda os macronutrientes, micronutrientes e como interpretar rótulos nutricionais.",
        categoria="nutricao",
        nivel="iniciante",
        duracao_horas=8,
        data_publicacao=timezone.now(),
        gratuito=True,
        preco=None
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/marmitas/Gemini_Generated_Image_aycpccaycpccaycp.jpg'):
        with open('media/marmitas/Gemini_Generated_Image_aycpccaycpccaycp.jpg', 'rb') as img_file:
            curso1.imagem.save('nutricao_fundamentos.jpg', File(img_file), save=False)
    
    curso1.save()
    print(f"Curso criado: {curso1}")
    
    # Intermediário
    curso2 = Curso(
        titulo="Nutrição Esportiva para Famílias Ativas",
        descricao="Curso focado em estratégias nutricionais para famílias que praticam esportes. Aprenda sobre alimentação pré e pós-treino, hidratação adequada e suplementação quando necessária.",
        categoria="nutricao",
        nivel="intermediario",
        duracao_horas=12,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('49.90')
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/marmitas/Gemini_Generated_Image_cfzki7cfzki7cfzk.jpg'):
        with open('media/marmitas/Gemini_Generated_Image_cfzki7cfzki7cfzk.jpg', 'rb') as img_file:
            curso2.imagem.save('nutricao_esportiva.jpg', File(img_file), save=False)
    
    curso2.save()
    print(f"Curso criado: {curso2}")
    
    # Avançado
    curso3 = Curso(
        titulo="Nutrição Terapêutica e Dietas Especiais",
        descricao="Curso avançado sobre nutrição aplicada a condições de saúde específicas como diabetes, hipertensão, doença celíaca e alergias alimentares. Aprenda a adaptar cardápios para necessidades especiais.",
        categoria="nutricao",
        nivel="avancado",
        duracao_horas=16,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('69.90')
    )
    curso3.save()
    print(f"Curso criado: {curso3}")
    
    # Criar cursos de Saúde
    # Iniciante
    curso4 = Curso(
        titulo="Primeiros Socorros Domésticos",
        descricao="Aprenda técnicas básicas de primeiros socorros para situações comuns em ambiente familiar. O curso aborda queimaduras, cortes, engasgamento, quedas e outras emergências domésticas.",
        categoria="saude",
        nivel="iniciante",
        duracao_horas=6,
        data_publicacao=timezone.now(),
        gratuito=True,
        preco=None
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/marmitas/Gemini_Generated_Image_puxbhfpuxbhfpuxb.jpg'):
        with open('media/marmitas/Gemini_Generated_Image_puxbhfpuxbhfpuxb.jpg', 'rb') as img_file:
            curso4.imagem.save('primeiros_socorros.jpg', File(img_file), save=False)
    
    curso4.save()
    print(f"Curso criado: {curso4}")
    
    # Intermediário
    curso5 = Curso(
        titulo="Saúde Mental Familiar",
        descricao="Curso que aborda estratégias para promover a saúde mental no ambiente familiar, identificar sinais de estresse, ansiedade e depressão, e técnicas de comunicação e apoio emocional.",
        categoria="saude",
        nivel="intermediario",
        duracao_horas=10,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('39.90')
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/marmitas/Gemini_Generated_Image_v9ktt0v9ktt0v9kt.jpg'):
        with open('media/marmitas/Gemini_Generated_Image_v9ktt0v9ktt0v9kt.jpg', 'rb') as img_file:
            curso5.imagem.save('saude_mental.jpg', File(img_file), save=False)
    
    curso5.save()
    print(f"Curso criado: {curso5}")
    
    # Avançado
    curso6 = Curso(
        titulo="Gerenciamento de Doenças Crônicas",
        descricao="Curso avançado sobre como gerenciar condições crônicas de saúde no ambiente familiar, incluindo diabetes, hipertensão, doenças cardíacas e respiratórias. Foco em cuidados contínuos e prevenção de complicações.",
        categoria="saude",
        nivel="avancado",
        duracao_horas=14,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('59.90')
    )
    curso6.save()
    print(f"Curso criado: {curso6}")
    
    # Criar cursos de Bem-estar
    # Iniciante
    curso7 = Curso(
        titulo="Meditação para Famílias",
        descricao="Introdução à prática de meditação adaptada para o contexto familiar. Aprenda técnicas simples que podem ser praticadas por adultos e crianças para reduzir o estresse e melhorar o bem-estar.",
        categoria="bem_estar",
        nivel="iniciante",
        duracao_horas=4,
        data_publicacao=timezone.now(),
        gratuito=True,
        preco=None
    )
    
    # Verificar se a imagem existe e associá-la
    if os.path.exists('media/marmitas/Gemini_Generated_Image_we3rhzwe3rhzwe3r.jpg'):
        with open('media/marmitas/Gemini_Generated_Image_we3rhzwe3rhzwe3r.jpg', 'rb') as img_file:
            curso7.imagem.save('meditacao_familia.jpg', File(img_file), save=False)
    
    curso7.save()
    print(f"Curso criado: {curso7}")
    
    # Intermediário
    curso8 = Curso(
        titulo="Yoga para Todas as Idades",
        descricao="Curso de yoga com práticas adaptadas para diferentes faixas etárias. Inclui sequências para praticar em família, promovendo flexibilidade, força e equilíbrio para todos.",
        categoria="bem_estar",
        nivel="intermediario",
        duracao_horas=8,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('34.90')
    )
    curso8.save()
    print(f"Curso criado: {curso8}")
    
    # Avançado
    curso9 = Curso(
        titulo="Terapias Integrativas para o Bem-estar Familiar",
        descricao="Curso avançado sobre diferentes abordagens terapêuticas complementares como aromaterapia, cromoterapia, musicoterapia e outras práticas que podem ser incorporadas na rotina familiar para promover bem-estar.",
        categoria="bem_estar",
        nivel="avancado",
        duracao_horas=12,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('54.90')
    )
    curso9.save()
    print(f"Curso criado: {curso9}")
    
    # Criar cursos de Tecnologia
    # Iniciante
    curso10 = Curso(
        titulo="Segurança Digital para Famílias",
        descricao="Aprenda como proteger sua família no ambiente digital. O curso aborda controle parental, segurança em redes sociais, proteção contra golpes online e boas práticas de privacidade digital.",
        categoria="tecnologia",
        nivel="iniciante",
        duracao_horas=6,
        data_publicacao=timezone.now(),
        gratuito=True,
        preco=None
    )
    curso10.save()
    print(f"Curso criado: {curso10}")
    
    # Intermediário
    curso11 = Curso(
        titulo="Tecnologia Assistiva para Necessidades Especiais",
        descricao="Curso sobre ferramentas e aplicativos tecnológicos que podem auxiliar pessoas com necessidades especiais. Ideal para famílias que buscam soluções tecnológicas para melhorar a qualidade de vida.",
        categoria="tecnologia",
        nivel="intermediario",
        duracao_horas=10,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('44.90')
    )
    curso11.save()
    print(f"Curso criado: {curso11}")
    
    # Avançado
    curso12 = Curso(
        titulo="Automação Residencial para Famílias",
        descricao="Curso avançado sobre como implementar soluções de casa inteligente que beneficiam toda a família. Aprenda sobre dispositivos IoT, assistentes virtuais e sistemas integrados para conforto e segurança.",
        categoria="tecnologia",
        nivel="avancado",
        duracao_horas=14,
        data_publicacao=timezone.now(),
        gratuito=False,
        preco=Decimal('64.90')
    )
    curso12.save()
    print(f"Curso criado: {curso12}")
    
    print("Criação de cursos concluída com sucesso!")