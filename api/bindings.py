from channels_api.bindings import ResourceBinding
from api.models import Chat, Message
from api.serializers import ChatDetailSerializer, MessageSerializer

class MessageBinding(ResourceBinding):
    model = Message
    stream = "messages"
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    
