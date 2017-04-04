from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class Chat(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    creator = models.ForeignKey(User, blank=False, null=True, db_constraint=False, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('title', 'creator',)

class Subscription(models.Model):
    user = models.ForeignKey(User, blank=False, null=False, related_name='subscriptions')
    chat = models.ForeignKey(Chat, blank=False, null=False, related_name='chats')

class Message(models.Model):
    author = models.ForeignKey(User, blank=False, null=True, db_constraint=False, related_name='messages')
    chat = models.ForeignKey(Chat, blank=False, null=False)
    text = models.TextField()
