from educacional.models import Curso, Videoaula
from django.utils import timezone
from django.core.files import File
import os

# Verificar se já existem videoaulas no banco de dados
if Videoaula.objects.count() > 0:
    print(f"Já existem {Videoaula.objects.count()} videoaulas no banco de dados. Pulando criação.")
else:
    # Obter cursos existentes para associar as videoaulas
    try:
        curso_nutricao_iniciante = Curso.objects.get(titulo="Fundamentos da Nutrição Saudável")
        curso_nutricao_intermediario = Curso.objects.get(titulo="Nutrição Esportiva para Famílias Ativas")
        curso_nutricao_avancado = Curso.objects.get(titulo="Nutrição Terapêutica e Dietas Especiais")
        
        curso_saude_iniciante = Curso.objects.get(titulo="Primeiros Socorros Domésticos")
        curso_saude_intermediario = Curso.objects.get(titulo="Saúde Mental Familiar")
        curso_saude_avancado = Curso.objects.get(titulo="Gerenciamento de Doenças Crônicas")
        
        curso_bem_estar_iniciante = Curso.objects.get(titulo="Meditação para Famílias")
        curso_bem_estar_intermediario = Curso.objects.get(titulo="Yoga para Todas as Idades")
        curso_bem_estar_avancado = Curso.objects.get(titulo="Terapias Integrativas para o Bem-estar Familiar")
        
        curso_tecnologia_iniciante = Curso.objects.get(titulo="Segurança Digital para Famílias")
        curso_tecnologia_intermediario = Curso.objects.get(titulo="Tecnologia Assistiva para Necessidades Especiais")
        curso_tecnologia_avancado = Curso.objects.get(titulo="Automação Residencial para Famílias")
        
        print("Cursos encontrados com sucesso!")
    except Curso.DoesNotExist:
        print("Erro: Alguns cursos não foram encontrados. Execute primeiro o script create_cursos.py")
        exit()
    
    # Criar videoaulas para o curso de Nutrição - Iniciante
    videoaula1 = Videoaula(
        titulo="Introdução aos Macronutrientes",
        descricao="Nesta aula, você aprenderá sobre os três macronutrientes essenciais: proteínas, carboidratos e gorduras. Entenda a função de cada um deles no organismo e como equilibrá-los em uma alimentação saudável para toda a família.",
        curso=curso_nutricao_iniciante,
        duracao_minutos=15,
        url_video="https://www.youtube.com/embed/jmzNXG2vPNs",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula1.save()
    print(f"Videoaula criada: {videoaula1}")
    
    videoaula2 = Videoaula(
        titulo="Como Interpretar Rótulos Nutricionais",
        descricao="Aprenda a ler e interpretar corretamente os rótulos nutricionais dos alimentos. Esta aula prática mostra como identificar ingredientes prejudiciais, entender as informações nutricionais e fazer escolhas mais saudáveis durante as compras.",
        curso=curso_nutricao_iniciante,
        duracao_minutos=18,
        url_video="https://www.youtube.com/embed/Orqjp2w5oHw",
        data_publicacao=timezone.now(),
        ordem=2
    )
    videoaula2.save()
    print(f"Videoaula criada: {videoaula2}")
    
    # Criar videoaulas para o curso de Nutrição - Intermediário
    videoaula3 = Videoaula(
        titulo="Nutrição Pré e Pós-Treino para Famílias Ativas",
        descricao="Descubra as melhores estratégias nutricionais para antes e depois dos exercícios físicos. Esta aula aborda as necessidades específicas de adultos e crianças ativos, com exemplos práticos de refeições e lanches ideais para otimizar o desempenho e a recuperação.",
        curso=curso_nutricao_intermediario,
        duracao_minutos=22,
        url_video="https://www.youtube.com/embed/pVXJQeTCMiw",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula3.save()
    print(f"Videoaula criada: {videoaula3}")
    
    # Criar videoaulas para o curso de Saúde - Iniciante
    videoaula4 = Videoaula(
        titulo="Primeiros Socorros em Caso de Engasgamento",
        descricao="Aprenda as técnicas corretas para agir em casos de engasgamento, uma das emergências domésticas mais comuns. Esta aula demonstra a manobra de Heimlich e outras intervenções para diferentes faixas etárias, desde bebês até idosos.",
        curso=curso_saude_iniciante,
        duracao_minutos=12,
        url_video="https://www.youtube.com/embed/PjC_m5Xaw8w",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula4.save()
    print(f"Videoaula criada: {videoaula4}")
    
    videoaula5 = Videoaula(
        titulo="Como Tratar Pequenos Cortes e Queimaduras",
        descricao="Esta aula prática ensina os procedimentos corretos para o tratamento imediato de pequenos cortes e queimaduras que podem ocorrer no ambiente doméstico. Aprenda a limpar, desinfetar e proteger ferimentos de forma adequada.",
        curso=curso_saude_iniciante,
        duracao_minutos=14,
        url_video="https://www.youtube.com/embed/s_-j-e_N9fk",
        data_publicacao=timezone.now(),
        ordem=2
    )
    videoaula5.save()
    print(f"Videoaula criada: {videoaula5}")
    
    # Criar videoaulas para o curso de Saúde Mental
    videoaula6 = Videoaula(
        titulo="Técnicas de Respiração para Redução de Ansiedade",
        descricao="Aprenda técnicas simples e eficazes de respiração que podem ser praticadas por toda a família para reduzir a ansiedade e o estresse. Esta aula demonstra exercícios práticos que podem ser incorporados na rotina diária.",
        curso=curso_saude_intermediario,
        duracao_minutos=16,
        url_video="https://www.youtube.com/embed/acUZdGd_3Gk",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula6.save()
    print(f"Videoaula criada: {videoaula6}")
    
    # Criar videoaulas para o curso de Bem-estar - Meditação
    videoaula7 = Videoaula(
        titulo="Meditação Guiada para Iniciantes",
        descricao="Uma introdução prática à meditação com uma sessão guiada de 10 minutos, ideal para quem nunca meditou. Aprenda a postura correta, técnicas de respiração e como lidar com distrações durante a prática.",
        curso=curso_bem_estar_iniciante,
        duracao_minutos=20,
        url_video="https://www.youtube.com/embed/Xl_B45DpMLU",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula7.save()
    print(f"Videoaula criada: {videoaula7}")
    
    videoaula8 = Videoaula(
        titulo="Meditação para Crianças: Abordagens Lúdicas",
        descricao="Descubra como introduzir a meditação para crianças de forma divertida e adequada à idade. Esta aula apresenta técnicas especialmente adaptadas, histórias guiadas e atividades que tornam a meditação acessível e atraente para os pequenos.",
        curso=curso_bem_estar_iniciante,
        duracao_minutos=18,
        url_video="https://www.youtube.com/embed/CvF9AEe-ozc",
        data_publicacao=timezone.now(),
        ordem=2
    )
    videoaula8.save()
    print(f"Videoaula criada: {videoaula8}")
    
    # Criar videoaulas para o curso de Yoga
    videoaula9 = Videoaula(
        titulo="Sequência de Yoga para Praticar em Família",
        descricao="Uma aula prática com uma sequência de yoga especialmente desenvolvida para ser praticada por adultos e crianças juntos. Posturas simples e divertidas que promovem a conexão familiar enquanto desenvolvem força e flexibilidade.",
        curso=curso_bem_estar_intermediario,
        duracao_minutos=25,
        url_video="https://www.youtube.com/embed/X655B4ISakg",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula9.save()
    print(f"Videoaula criada: {videoaula9}")
    
    # Criar videoaulas para o curso de Tecnologia - Segurança Digital
    videoaula10 = Videoaula(
        titulo="Configurando Controle Parental em Dispositivos",
        descricao="Um guia passo a passo para configurar ferramentas de controle parental em smartphones, tablets e computadores. Aprenda a proteger seus filhos de conteúdos inadequados e gerenciar o tempo de tela de forma saudável.",
        curso=curso_tecnologia_iniciante,
        duracao_minutos=19,
        url_video="https://www.youtube.com/embed/1YXuZG6vYnE",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula10.save()
    print(f"Videoaula criada: {videoaula10}")
    
    videoaula11 = Videoaula(
        titulo="Como Identificar e Evitar Golpes Online",
        descricao="Esta aula ensina a reconhecer os sinais de phishing, golpes em redes sociais e outras ameaças digitais comuns. Aprenda estratégias práticas para proteger sua família e seus dados pessoais no ambiente online.",
        curso=curso_tecnologia_iniciante,
        duracao_minutos=17,
        url_video="https://www.youtube.com/embed/0u69vy-hV8o",
        data_publicacao=timezone.now(),
        ordem=2
    )
    videoaula11.save()
    print(f"Videoaula criada: {videoaula11}")
    
    # Criar videoaulas para o curso de Tecnologia Assistiva
    videoaula12 = Videoaula(
        titulo="Aplicativos de Acessibilidade para Necessidades Especiais",
        descricao="Conheça os melhores aplicativos e ferramentas digitais que podem auxiliar pessoas com diferentes necessidades especiais. Esta aula apresenta soluções para deficiências visuais, auditivas, motoras e cognitivas.",
        curso=curso_tecnologia_intermediario,
        duracao_minutos=23,
        url_video="https://www.youtube.com/embed/wBJRw2X-eNI",
        data_publicacao=timezone.now(),
        ordem=1
    )
    videoaula12.save()
    print(f"Videoaula criada: {videoaula12}")
    
    print("Criação de videoaulas concluída com sucesso!")