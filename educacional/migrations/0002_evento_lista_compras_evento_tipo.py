# Generated by Django 4.2.20 on 2025-03-12 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('educacional', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='lista_compras',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='eventos', to='educacional.listacompras'),
        ),
        migrations.AddField(
            model_name='evento',
            name='tipo',
            field=models.CharField(choices=[('pessoal', 'Pessoal'), ('familiar', 'Familiar'), ('trabalho', 'Trabalho'), ('saude', 'Saúde'), ('outro', 'Outro')], default='pessoal', max_length=20),
        ),
    ]
