from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from api.models import Chat, Message, Profile
from api.serializers import ChatSerializer, UserSerializer, MessageSerializer, ChatDetailSerializer, ProfileSerializer
from rest_framework.response import Response
from rest_framework import status, generics, views
from rest_framework.authtoken.models import Token
from django.forms.models import model_to_dict
from rest_framework.authtoken.views import ObtainAuthToken
import json

@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def create_user(request):
    serialized = UserSerializer(data=request.data, context={'request': request})
    if serialized.is_valid():
        #new user
        user = User(
            username=request.data['username'],
            email=request.data['email'],
        )
        print(serialized)
        user.set_password(request.data['password'])
        user.save()

        #new default profile
        profile = Profile.objects.create(user=user, preferred_lang='en')
        profile.save()

        # user = serialized.create(serialized.data)
        serialized = UserSerializer(user)
        token = model_to_dict(Token.objects.create(user=user))
        return Response({'user': serialized.data, 'token': token}, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key,
                         'username': token.user.username,
                         'user_id': token.user.id,
                         'lang': token.user.profile.preferred_lang,
                         'email': token.user.email})

class ChatList(generics.ListCreateAPIView):
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return user.subscriptions.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            self.serializer_class = ChatDetailSerializer
        if self.request.method == 'GET':
            self.serializer_class = ChatSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        data = request.data.copy()
        users = map(int, json.loads(data.get('subscribers', '')))

        invited_users = [ user for user in User.objects.filter(id__in=users) ]
        serializer = serializer(
            data=data,
            context={
                'users': invited_users,
                'creator': request.user,
            })

        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            for user in serializer.data['subscribers']:
                if 'password' in user:
                    del user['password']
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


    def perform_create(self, serializer):
        serializer.save()

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return user.subscriptions.all()

class SearchList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return User.objects.filter(username__icontains=username)

class MessageDetail(generics.ListCreateAPIView):
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=User.objects.get(id=self.request.user.id),
            chat=Chat.objects.get(id=self.request.data.get('chat_id'))
        )

class ProfileDetail(views.APIView):
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, many=False, context={'request': request})
        return Response(serializer.data)
