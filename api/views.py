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
from google.cloud import translate
import json, os
import google.auth

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
        users = map(int, data.get('subscribers', '').split(' '))
        # users = data.get('subscribers', '')
        invited_users = [ user for user in User.objects.filter(id__in=users) ]
        invited_dicts = [ model_to_dict(user) for user in invited_users ]
        data.__setitem__('subscribers', invited_dicts)

        serializer = serializer(
            data=data,
            context={
                'users': invited_users,
                'creator': request.user,
                'request': request
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
        language = self.request.query_params.get('language', None)
        return user.subscriptions.all()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        fields = ['author','created_at','text']
        if self.request.method == 'GET':
            query_fields = self.request.query_params.get('language', None)

            if query_fields:
                fields = set(fields + query_fields.split(','))

        kwargs['context'] = self.get_serializer_context()
        kwargs['context']['request'] = self.request

        serializer = serializer_class(*args, **kwargs)
        msgs = dict(next(iter(serializer.data['messages'] or []), {}))

        if any(msgs):
            for field in msgs.keys():
                for msg in serializer.data['messages']:
                    if field in msg and field not in fields:
                        del msg[field]

        return serializer

    def destroy(self, request, pk, *args, **kwargs):
        user = request.user
        chat = Chat.objects.get(id=pk)
        user.subscriptions.remove(chat)
        chat.subscribers.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

class SearchList(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return User.objects.filter(username__icontains=username)

class MessageDetail(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    AVAILABLE_LANGUAGES = ('en', 'es', 'de', 'ru', 'ja')

    def translate(self, text, src_lang, target_lang):
        credentials, project = google.auth.default()
        client = translate.Client(credentials=credentials)
        if(src_lang==target_lang):
            return text
        else:
            result = client.translate(
                values=text,
                target_language=target_lang,
                source_language=src_lang
            )
            return result['translatedText']

    def perform_create(self, serializer):
        user = User.objects.get(id=self.request.user.id)
        src_language = self.request.data.get('language')
        text = self.request.data.get('text')

        en_text = self.translate(text, src_language, 'en')
        es_text = self.translate(text, src_language, 'es')
        de_text = self.translate(text, src_language, 'de')
        ru_text = self.translate(text, src_language, 'ru')
        ja_text = self.translate(text, src_language, 'ja')

        serializer.save(
            author=user,
            chat=Chat.objects.get(id=self.request.data.get('chat_id')),
            text=text,
            en_text=en_text,
            es_text=es_text,
            de_text=de_text,
            ru_text=ru_text,
            ja_text=ja_text
        )

class ProfileDetail(views.APIView):
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, format=None):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
