# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-09-17 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizacion', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='License',
            new_name='Licensor',
        ),
        migrations.RemoveField(
            model_name='anime',
            name='license',
        ),
        migrations.AddField(
            model_name='anime',
            name='licensor',
            field=models.ManyToManyField(related_name='anime_licensors', to='visualizacion.Licensor'),
        ),
        migrations.AlterField(
            model_name='anime',
            name='name_japanese',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='anime',
            name='status',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.RemoveField(
            model_name='anime',
            name='studios',
        ),
        migrations.AddField(
            model_name='anime',
            name='studios',
            field=models.ManyToManyField(related_name='anime_studio', to='visualizacion.Studio'),
        ),
    ]
