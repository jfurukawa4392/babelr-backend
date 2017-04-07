from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from api import views

urlpatterns = [
    url(r'^auth-token/', obtain_auth_token),
    url(r'^chats/$', views.ChatList.as_view()),
    url(r'^chats/(?P<pk>[0-9]+)/$', views.ChatDetail.as_view()),
    url(r'^profile/$', views.ProfileDetail.as_view()),
    url(r'^users/', views.create_user),
    url(r'^messages/', views.MessageDetail.as_view()),
    url(r'^search', views.SearchList.as_view())
]
