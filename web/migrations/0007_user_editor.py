# Generated by Django 2.0.2 on 2018-09-25 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_user_propiedades'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='editor',
            field=models.CharField(choices=[('summernote', 'Summernote'), ('ckeditor', 'Ckeditor')], default='summernote', max_length=30, verbose_name='editor'),
        ),
    ]
