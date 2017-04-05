from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from api.models import Chat
from api.serializers import ChatSerializer, UserSerializer, MessageSerializer, ChatDetailSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from django.forms.models import model_to_dict
from rest_framework import viewsets

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def create_user(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user = serialized.create(serialized)
        token = model_to_dict(Token.objects.create(user=user))
        user = model_to_dict(user)
        token['username'] = user['username']
        token['email'] = user['email']
        token['name'] = user['first_name'] + ' ' + user['last_name']
        return Response({'user': token}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class ChatList(generics.ListCreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        print(self.request)
        user = self.request.user
        return user.subscriptions.all()

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return user.subscriptions.all()
