from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.models import Chat, Message, Profile

class DynamicFieldsSerializerMixin(object):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsSerializerMixin, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                print(self.fields)

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

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        many=False,
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ( 'user', 'preferred_lang', 'avatar_url')

class ChatSerializer(serializers.ModelSerializer):

    subscribers = UserSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'created_at', 'title', 'subscribers')

class SubscriberSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=15)
    id = serializers.IntegerField()
    avatar_url = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        source='profile',
        slug_field='avatar_url'
    )
    # profile = ProfileSerializer(
    #     many=False,
    #     read_only=True)

class MessageSerializer(serializers.ModelSerializer):
    author = SubscriberSerializer(
        many=False,
        read_only=True
    )

    # serializers.SubscriberSerializer(
    #     many=False,
    #     read_only=True
    # )

    avatar = ProfileSerializer(
        many=False,
        read_only=True,
        source='profile'
    )

    class Meta:
        model = Message
        fields = ('created_at', 'author', 'avatar', 'text', 'en_text', 'es_text',
            'de_text', 'ru_text', 'ja_text')

class ChatDetailSerializer(serializers.ModelSerializer):
    subscribers = SubscriberSerializer(many=True)

    messages = MessageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Chat
        fields = ('id', 'created_at', 'title', 'subscribers', 'messages')

    def create(self, validated_data):
        subscribers_data = self.context['users']

        chat = Chat(
            title=validated_data['title'],
            creator=self.context['creator']
        )
        chat.save()

        chat.subscribers.add(self.context['creator'])
        for subscriber in subscribers_data:
            chat.subscribers.add(subscriber)
            subscriber.subscriptions.add(chat)
        return chat
