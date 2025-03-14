# Generated by Django 4.2.20 on 2025-03-10 17:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GrupoApoio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('tipo', models.CharField(max_length=50)),
                ('local', models.TextField(blank=True)),
                ('horario', models.CharField(blank=True, max_length=100)),
                ('contato', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Grupo de Apoio',
                'verbose_name_plural': 'Grupos de Apoio',
                'ordering': ['nome'],
            },
        ),
        migrations.CreateModel(
            name='ContatoEmergencial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('familiar', 'Familiar'), ('amigo', 'Amigo'), ('medico', 'Médico'), ('cuidador', 'Cuidador'), ('outro', 'Outro')], max_length=20)),
                ('telefone', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="O número de telefone deve estar no formato: '+999999999'. Até 15 dígitos são permitidos.", regex='^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('endereco', models.TextField(blank=True)),
                ('observacoes', models.TextField(blank=True)),
                ('prioridade', models.IntegerField(default=5, help_text='Prioridade de 1 a 5 (1 é a mais alta)')),
                ('acionamento_rapido', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contatos_emergenciais', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Contato Emergencial',
                'verbose_name_plural': 'Contatos Emergenciais',
                'ordering': ['prioridade', 'nome'],
            },
        ),
        migrations.CreateModel(
            name='AcionamentoEmergencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora', models.DateTimeField(auto_now_add=True)),
                ('motivo', models.TextField(blank=True)),
                ('atendido', models.BooleanField(default=False)),
                ('observacoes', models.TextField(blank=True)),
                ('contato', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acionamentos', to='rede_apoio.contatoemergencial')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='acionamentos_emergencia', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Acionamento de Emergência',
                'verbose_name_plural': 'Acionamentos de Emergência',
                'ordering': ['-data_hora'],
            },
        ),
    ]
