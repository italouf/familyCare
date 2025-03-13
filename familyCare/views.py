from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from educacional.views import get_random_courses
from tarefas.models import Tarefa

def home(request):
    context = {}
    if request.user.is_authenticated:
        # Get random courses for the educational content widget
        context['random_courses'] = get_random_courses()
        # Get user's tasks
        context['tarefas'] = Tarefa.objects.filter(usuario=request.user).order_by('prazo')
    return render(request, 'home.html', context)