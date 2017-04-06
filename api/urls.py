from django.conf.urls import url, include
from rest_framework import routers
from api import views

urlpatterns = [
    url(r'^chats/$', views.ChatList.as_view()),
    url(r'^chats/(?P<pk>[0-9]+)/$', views.ChatDetail.as_view()),
    url(r'^users/', views.create_user),
    url(r'^messages/', views.MessageDetail.as_view()),
]
