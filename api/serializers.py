from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import Chat, Message, Profile


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
        write_only=True
    )

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(min_length=8, write_only=True)

    profile = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        # queryset=Profile.objects.all(),
        slug_field='preferred_lang',
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
            'profile': {'read_only': True}
        }

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data.data['username'],
    #         email=validated_data.data['email'],
    #     )
    #     user.set_password(serialized.data['password'])
    #     user.save()
    #     return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        many=False,
    )

    class Meta:
        model = Profile
        fields = ( 'user', 'preferred_lang', 'avatar_url')

class ChatSerializer(serializers.ModelSerializer):
    subscribers = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'created_at', 'title', 'subscribers')

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
     )

    # chat = serializers.PrimaryKeyRelatedField(
    #     many=False,
    #     read_only=True,
    # )

    class Meta:
        model = Message
        fields = ('created_at', 'author', 'text')

class ChatDetailSerializer(serializers.ModelSerializer):
    subscribers = UserSerializer(many=True)

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'created_at', 'title', 'subscribers', 'messages')

    def create(self, validated_data):
        subscribers_data = self.context['users']
        if 'messages' in validated_data:
            message_data = validated_data['messages']
        else:
            message_data = ''
        chat = Chat(
            title=validated_data['title'],
            creator=self.context['creator']
        )
        chat.save()
        initial_message = Message(
            author=self.context['creator'],
            chat=chat,
            text=message_data
        )
        initial_message.save()
        chat.subscribers.add(self.context['creator'])
        for subscriber in subscribers_data:
            chat.subscribers.add(subscriber)
            subscriber.subscriptions.add(chat)
        return chat
