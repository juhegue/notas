# Generated by Django 3.1.2 on 2022-10-09 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0015_agendaevento_agendaeventocolor_agendaeventoprdefinido'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendaevento',
            name='aviso_email',
            field=models.BooleanField(default=False, verbose_name='Avisar con email'),
        ),
    ]
