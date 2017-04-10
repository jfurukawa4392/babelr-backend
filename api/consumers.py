import json
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from api.models import Chat, Message
from api.views import ChatDetail, MessageDetail
from django.http import HttpResponse
from channels.handler import AsgiHandler

def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)

@channel_session
def ws_connect(message):
    print(message)
    prefix, chat_id = message['path'].strip('/').split('/')
    chat = Chat.objects.get(id=chat_id)
    Group('chat-' + chat_id).add(message.reply_channel)
    message.channel_session['chat'] = chat.id

@channel_session
def ws_receive(message):
    print(message)
    chat_id = message.channel_session['chat']
    room = Chat.objects.get(id=chat_id)
    data = json.loads(message['text'])
    m = Chat.messages.create(
        handle=data['handle'],
        message=data['message']
    )
    Group('chat-'+chat_id).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    chat_id = message.channel_session['chat']
    Group('chat-'+chat_id).discard(message.reply_channel)
