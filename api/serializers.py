from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import Chat, Message

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    username = serializers.CharField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'].value,
            email=validated_data['email'].value,
        )
        user.set_password(validated_data['password'].value)
        user.save()
        return user


class ChatSerializer(serializers.ModelSerializer):
    subscribers = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
     )

    class Meta:
        model = Chat
        fields = ('id', 'created_at', 'title', 'subscribers')

class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
     )
    class Meta:
        model = Message
        fields = ('id', 'created_at', 'author', 'text')

class ChatDetailSerializer(serializers.ModelSerializer):
    subscribers = serializers.SlugRelatedField(
    many=True,
    queryset=User.objects.all(),
    slug_field='username'
    )
    # UserSerializer?

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ('id', 'created_at', 'title', 'subscribers', 'messages')
