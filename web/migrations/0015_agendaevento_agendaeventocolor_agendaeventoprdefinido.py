# Generated by Django 3.1.2 on 2022-10-09 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_auto_20221008_2325'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgendaEventoColor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(editable=False, verbose_name='Creado')),
                ('modificado', models.DateTimeField(verbose_name='Actualizado')),
                ('color', models.CharField(max_length=7, verbose_name='Color')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Agenda evento color',
                'verbose_name_plural': 'Agenda evento colores',
            },
        ),
        migrations.CreateModel(
            name='AgendaEventoPrdefinido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(editable=False, verbose_name='Creado')),
                ('modificado', models.DateTimeField(verbose_name='Actualizado')),
                ('inicio', models.CharField(default='00:00', max_length=5, verbose_name='Hora inicio')),
                ('duracion', models.PositiveIntegerField(default=0, verbose_name='Minutos duración')),
                ('titulo', models.TextField(verbose_name='Título')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.agendaeventocolor', verbose_name='Color')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Agenda evento predefinido',
                'verbose_name_plural': 'Agenda eventos predefinidos',
            },
        ),
        migrations.CreateModel(
            name='AgendaEvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(editable=False, verbose_name='Creado')),
                ('modificado', models.DateTimeField(verbose_name='Actualizado')),
                ('inicio', models.DateTimeField(verbose_name='Inicio evento')),
                ('fin', models.DateTimeField(verbose_name='Fin evento')),
                ('titulo', models.TextField(verbose_name='Título')),
                ('dia_completo', models.BooleanField(default=True, verbose_name='Todo el día')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.agendaeventocolor', verbose_name='Color')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Agenda evento',
                'verbose_name_plural': 'Agenda eventos',
            },
        ),
    ]
