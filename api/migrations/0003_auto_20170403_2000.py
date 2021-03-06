# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 20:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_chat_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='chat',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('title', 'creator')]),
        ),
    ]
