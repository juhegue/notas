# Generated by Django 3.1.2 on 2022-10-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_auto_20201018_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='libro',
            name='privado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='nota',
            name='privada',
            field=models.BooleanField(default=False),
        ),
    ]
