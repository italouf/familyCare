"""URL configuration for familyCare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from templates.registration.views import register_view
from rede_apoio.models import ContatoEmergencial
from tarefas.models import ServicoBaba
from educacional.models import Evento
from django.utils import timezone
from django.shortcuts import render
from django.db.models import Sum
from saude.models import ConsumoAgua, MetaAgua, AtividadeFisica
from nutricao.models import Marmita
from datetime import datetime, time

def home_view(request):
    context = {}
    
    # Get random courses for educational content section
    from educacional.views import get_random_courses
    context['random_courses'] = get_random_courses()
    
    if request.user.is_authenticated:
        # Get emergency contacts
        context['emergency_contacts'] = ContatoEmergencial.objects.filter(usuario=request.user)
        
        # Get babysitting services
        today = timezone.now().date()
        context['babysitting_services'] = ServicoBaba.objects.filter(
            usuario=request.user,
            data__gte=today
        ).order_by('data')
        
        # Get today's events
        context['daily_events'] = Evento.objects.filter(
            data_inicio__date=today
        ).order_by('data_inicio')
        
        # Get water consumption data
        consumos_hoje = ConsumoAgua.objects.filter(usuario=request.user, data=today)
        total_hoje = consumos_hoje.aggregate(total=Sum('quantidade_ml'))['total'] or 0
        
        try:
            meta_agua = MetaAgua.objects.get(usuario=request.user)
            meta_diaria = meta_agua.quantidade_diaria_ml
        except MetaAgua.DoesNotExist:
            meta_diaria = 2000
        
        context['water_consumed'] = total_hoje
        context['water_goal'] = meta_diaria
        context['water_percentage'] = min(int((total_hoje / meta_diaria) * 100), 100) if meta_diaria > 0 else 0
        
        # Get latest physical activity
        context['last_activity'] = AtividadeFisica.objects.filter(usuario=request.user).order_by('-data').first()
        
        # Get recommended meals based on current time
        current_time = timezone.localtime().time()
        if time(6, 0) <= current_time <= time(10, 0):
            meal_type = 'cafe_manha'
        elif time(11, 0) <= current_time <= time(14, 0):
            meal_type = 'almoco'
        elif time(18, 0) <= current_time <= time(22, 0):
            meal_type = 'jantar'
        else:
            meal_type = 'lanche'
            
        context['recommended_meals'] = Marmita.objects.filter(
            disponivel=True,
            tipo_refeicao=meal_type
        ).order_by('?')[:4]
    
    return render(request, 'home.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('sobre/', TemplateView.as_view(template_name='sobre.html'), name='sobre'),
    path('contato/', TemplateView.as_view(template_name='contato.html'), name='contato'),
    path('perfil/', TemplateView.as_view(template_name='perfil.html'), name='perfil'),
    
    # Autenticação
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', register_view, name='register'),
    
    # Módulos do sistema
    path('saude/', include('saude.urls', namespace='saude')),
    path('nutricao/', include('nutricao.urls', namespace='nutricao')),
    path('rede-apoio/', include('rede_apoio.urls', namespace='rede_apoio')),
    path('modo-noturno/', include('modo_noturno.urls', namespace='modo_noturno')),
    path('educacional/', include('educacional.urls', namespace='educacional')),
    path('tarefas/', include('tarefas.urls', namespace='tarefas')),
    path('mercado/', include('mercado.urls', namespace='mercado')),
    path('entretenimento/', include('entretenimento.urls', namespace='entretenimento')),
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
