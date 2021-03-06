from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
import random

class Chat(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    creator = models.ForeignKey(User, blank=False, null=True, db_constraint=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subscribers = models.ManyToManyField(User, related_name='subscriptions')

    class Meta:
        unique_together = ('title', 'creator')

class Message(models.Model):
    author = models.ForeignKey(User, blank=False, null=True, db_constraint=False)
    chat = models.ForeignKey(Chat, blank=False, null=False, related_name='messages')
    text = models.TextField(blank=False)
    en_text = models.TextField(blank=True, null=True, default='')
    es_text = models.TextField(blank=True, null=True, default='')
    de_text = models.TextField(blank=True, null=True, default='')
    ru_text = models.TextField(blank=True, null=True, default='')
    ja_text = models.TextField(blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    preferred_lang = models.CharField(max_length=2, null=False, blank=False)
    avatar_url = models.URLField(blank=True, null=False, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user.first_name + self.user.last_name

DEFAULT_AVATAR_URLS = [
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/1_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/2_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/3_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/4_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/5_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/6_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/7_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/8_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/9_avatar.png",
    "https://s3-us-west-1.amazonaws.com/babelr/default_avatars/10_avatar.png"
]

def random_avatar():
    return random.choice(DEFAULT_AVATAR_URLS)

@receiver(models.signals.post_save, sender=User)
def save_profile(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance, preferred_lang='en', avatar_url=random_avatar())
        profile.save()
