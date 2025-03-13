from django.contrib import admin
from .models import Curso, InscricaoCurso, Ebook, Videoaula

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'nivel', 'duracao_horas', 'data_publicacao', 'gratuito')
    list_filter = ('categoria', 'nivel', 'gratuito')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_publicacao'

@admin.register(InscricaoCurso)
class InscricaoCursoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'data_inscricao', 'concluido')
    list_filter = ('concluido', 'data_inscricao')
    search_fields = ('usuario__username', 'curso__titulo')
    date_hierarchy = 'data_inscricao'

@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'paginas', 'gratuito')
    list_filter = ('categoria', 'gratuito')
    search_fields = ('titulo', 'autor', 'descricao')

@admin.register(Videoaula)
class VideoaulaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'duracao_minutos', 'data_publicacao')
    list_filter = ('curso', 'data_publicacao')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_publicacao'
