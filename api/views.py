from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from api.models import Chat
from api.serializers import ChatSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from django.forms.models import model_to_dict
from rest_framework.views import APIView


@api_view(['GET', 'POST'])
def chat_list(request):
    """
    List all code chats, or create a new chat.
    """
    if request.method == 'GET':
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def chat_detail(request, pk):
    try:
        chat = Chat.objects.get(pk=pk)
    except Chat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ChatSerializer(chat)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ChatSerializer(chat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        chat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        print(serialized)
        user = serialized.create(serialized)
        token = model_to_dict(Token.objects.create(user=user))
        user = model_to_dict(user)
        token['username'] = user['username']
        token['email'] = user['email']
        token['name'] = user['first_name'] + ' ' + user['last_name']
        return Response({'user': token}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class ChatList(generics.ListAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self, format=None):
        user = self.request.user
        return user.chats.all()
