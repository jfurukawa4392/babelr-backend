# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-07 20:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_profile_avatar_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='de_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='en_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='es_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AddField(
            model_name='message',
            name='ru_text',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
