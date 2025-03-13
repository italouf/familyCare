# Generated by Django 4.2.20 on 2025-03-10 20:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rede_apoio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParticipacaoGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_entrada', models.DateTimeField(default=django.utils.timezone.now)),
                ('ativo', models.BooleanField(default=True)),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participantes', to='rede_apoio.grupoapoio')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participacoes_grupos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Participação em Grupo',
                'verbose_name_plural': 'Participações em Grupos',
                'unique_together': {('usuario', 'grupo')},
            },
        ),
    ]
