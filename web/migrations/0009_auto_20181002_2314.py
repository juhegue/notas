# Generated by Django 2.0.2 on 2018-10-02 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_auto_20180926_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='editor',
            field=models.CharField(choices=[('summernote', 'Summernote'), ('ckeditor', 'Ckeditor'), ('froala', 'Froala'), ('trumbowyg', 'Trumbowyg')], default='summernote', max_length=30, verbose_name='editor'),
        ),
    ]
