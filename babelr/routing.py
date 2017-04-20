from api import consumers
from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route
# from channels import route
from api.bindings import MessageBinding

class APIDemultiplexer(WebsocketDemultiplexer):

    consumers = {
      'messages': MessageBinding.consumer
    }

channel_routing = [
    route("websocket.connect", consumers.ws_connect),
    route("websocket.receive", consumers.ws_receive),
    # route('websocket.receive', consumers.ws_receive),
    # route("websocket.disconnect", consumers.ws_disconnect)
]
