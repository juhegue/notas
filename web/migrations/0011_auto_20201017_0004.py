# Generated by Django 3.1.2 on 2020-10-17 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_adjuntotemporal'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjuntotemporal',
            name='adjunto_borrado_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='adjuntotemporal',
            name='uuid_id',
            field=models.UUIDField(db_index=True),
        ),
    ]
