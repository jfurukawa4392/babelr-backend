from django.conf.urls import url, include
from rest_framework import routers
from api import views

urlpatterns = [
    url(r'^chats/$', views.chat_list),
    url(r'^chats/(?P<pk>[0-9]+)/$', views.chat_detail),
    url(r'^users/register', views.create_user),
]
