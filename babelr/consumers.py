import json
from channels import Group
from channels.sessions import channel_session
from api.models import Chat

@channel_session
def ws_connect(message):
    prefix, chat_id = message['path'].strip('/').split('/')
    chat = Chat.objects.get(id=chat_id)
    Group('chat-' + chat_id).add(message.reply_channel)
    message.channel_session['chat'] = chat.id

@channel_session
def ws_receive(message):
    chat_id = message.channel_session['chat']
    room = Room.objects.get(id=chat_id)
    data = json.loads(message['text'])
    m = Chat.messages.create(handle=data['handle'], message=data['message'])
    Group('chat-'+chat_id).send({'text': json.dumps(m.as_dict())})

@channel_session
def ws_disconnect(message):
    chat_id = message.channel_session['chat']
    Group('chat-'+chat_id).discard(message.reply_channel)
