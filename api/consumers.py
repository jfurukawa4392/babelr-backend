import json
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from api.models import Chat, Message
from api.views import ChatDetail, MessageDetail
from channels.handler import AsgiHandler
from django.forms.models import model_to_dict

@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    print('')
    print(message)
    print(message['path'])
    print(message.user)
    prefix, chat_id = message['path'].strip('/').split('/')
    chat = Chat.objects.get(id=chat_id)
    print(chat.title)
    print(chat_id)
    Group('chat-' + chat_id).add(message.reply_channel)
    print(Group('chat-' + chat_id))
    message.channel_session['chat'] = chat.id

@channel_session_user
def ws_receive(message):
    print('received message!')
    print(message['text'])
    chat_id = message.channel_session['chat']
    chat = Chat.objects.get(id=chat_id)
    print(chat_id)
    data = message['text']
    m = chat.messages.last()
    Group('chat-'+str(chat_id)).send({'text': json.dumps(model_to_dict(m))})

def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    print('received message!')
    print(message['text'])
    message.reply_channel.send({
        "text": 'suhhhhhh',
    })

# @channel_session_user
def ws_disconnect(message):
    print('')
    print('disconnecting...')
    chat_id = message.channel_session['chat']
    Group('chat-'+str(chat_id)).discard(message.reply_channel)
