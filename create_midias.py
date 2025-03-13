from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.models import User
from entretenimento.models import Midia
import os
import requests
from datetime import datetime

def create_midia(titulo, tipo, categoria, descricao, ano_lancamento, duracao_minutos,
               link_streaming, artista_autor, classificacao, imagem_url):
    try:
        # Download the image from URL
        img_temp = NamedTemporaryFile()
        response = requests.get(imagem_url)
        img_temp.write(response.content)
        img_temp.flush()

        midia = Midia.objects.create(
            titulo=titulo,
            tipo=tipo,
            categoria=categoria,
            descricao=descricao,
            ano_lancamento=ano_lancamento,
            duracao_minutos=duracao_minutos,
            link_streaming=link_streaming,
            artista_autor=artista_autor,
            classificacao=classificacao
        )

        # Save the image
        filename = os.path.basename(imagem_url)
        midia.imagem.save(filename, File(img_temp))
        return midia
    except Exception as e:
        print(f"Error creating media {titulo}: {str(e)}")
        return None

def populate_midias():
    # Filmes
    create_midia(
        titulo="Interestelar",
        tipo="filme",
        categoria="ficcao",
        descricao="Uma equipe de exploradores viaja através de um buraco de minhoca em busca de um novo lar para a humanidade.",
        ano_lancamento=2014,
        duracao_minutos=169,
        link_streaming="https://www.netflix.com/title/70305903",
        artista_autor="Christopher Nolan",
        classificacao="12",
        imagem_url="https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg"
    )

    create_midia(
        titulo="O Poderoso Chefão",
        tipo="filme",
        categoria="drama",
        descricao="A história da família Corleone sob a perspectiva do patriarca Vito Corleone e seu filho Michael.",
        ano_lancamento=1972,
        duracao_minutos=175,
        link_streaming="https://www.primevideo.com/detail/0HBID59JGPH8OZQE0PBXN6TVKJ",
        artista_autor="Francis Ford Coppola",
        classificacao="14",
        imagem_url="https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg"
    )

    # Séries
    create_midia(
        titulo="Breaking Bad",
        tipo="serie",
        categoria="drama",
        descricao="Um professor de química do ensino médio se transforma em um implacável produtor de metanfetamina.",
        ano_lancamento=2008,
        duracao_minutos=45,
        link_streaming="https://www.netflix.com/title/70143836",
        artista_autor="Vince Gilligan",
        classificacao="16",
        imagem_url="https://m.media-amazon.com/images/M/MV5BYmQ4YWMxYjUtNjZmYi00MDQ1LWFjMjMtNjA5ZDdiYjdiODU5XkEyXkFqcGdeQXVyMTMzNDExODE5._V1_.jpg"
    )

    create_midia(
        titulo="Stranger Things",
        tipo="serie",
        categoria="ficcao",
        descricao="Quando um garoto desaparece, uma pequena cidade descobre um mistério envolvendo experimentos secretos.",
        ano_lancamento=2016,
        duracao_minutos=50,
        link_streaming="https://www.netflix.com/title/80057281",
        artista_autor="Duffer Brothers",
        classificacao="14",
        imagem_url="https://m.media-amazon.com/images/M/MV5BMDZkYmVhNjMtNWU4MC00MDQxLWE3MjYtZGMzZWI1ZjhlOWJmXkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_.jpg"
    )

    # Músicas
    create_midia(
        titulo="Bohemian Rhapsody",
        tipo="musica",
        categoria="musical",
        descricao="Uma das músicas mais icônicas do rock, misturando elementos de ópera e rock progressivo.",
        ano_lancamento=1975,
        duracao_minutos=6,
        link_streaming="https://open.spotify.com/track/3z8h0TU7ReDPLIbEnYhWZb",
        artista_autor="Queen",
        classificacao="L",
        imagem_url="https://m.media-amazon.com/images/M/MV5BNDgwNTQ5MDYyM15BMl5BanBnXkFtZTgwNTM3NzYxNzM@._V1_.jpg"
    )

    create_midia(
        titulo="Garota de Ipanema",
        tipo="musica",
        categoria="musical",
        descricao="Uma das músicas brasileiras mais conhecidas internacionalmente, um clássico da Bossa Nova.",
        ano_lancamento=1962,
        duracao_minutos=5,
        link_streaming="https://open.spotify.com/track/3kKVqFF4pv4EXeQe428zl2",
        artista_autor="Tom Jobim & Vinícius de Moraes",
        classificacao="L",
        imagem_url="https://m.media-amazon.com/images/I/71UT9QDXHIL._AC_UF1000,1000_QL80_.jpg"
    )

    # Jogos
    create_midia(
        titulo="The Legend of Zelda: Breath of the Wild",
        tipo="jogo",
        categoria="aventura",
        descricao="Um jogo de aventura em mundo aberto que redefiniu o gênero com sua liberdade de exploração.",
        ano_lancamento=2017,
        duracao_minutos=None,
        link_streaming="https://www.nintendo.com/games/detail/the-legend-of-zelda-breath-of-the-wild-switch",
        artista_autor="Nintendo",
        classificacao="10",
        imagem_url="https://m.media-amazon.com/images/M/MV5BMTc5OTk4MTM3M15BMl5BanBnXkFtZTgwMDg1NDcyMTI@._V1_.jpg"
    )

    create_midia(
        titulo="Red Dead Redemption 2",
        tipo="jogo",
        categoria="acao",
        descricao="Uma épica história de lealdade e sobrevivência no coração da América em 1899.",
        ano_lancamento=2018,
        duracao_minutos=None,
        link_streaming="https://store.steampowered.com/app/1174180/Red_Dead_Redemption_2/",
        artista_autor="Rockstar Games",
        classificacao="18",
        imagem_url="https://m.media-amazon.com/images/M/MV5BMjA5MDM3NTY4M15BMl5BanBnXkFtZTgwNDk2MjI0NjM@._V1_.jpg"
    )

if __name__ == '__main__':
    populate_midias()
    print("Entertainment media populated successfully!")