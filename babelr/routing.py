from api import consumers
from channels.generic.websockets import WebsocketDemultiplexer
from channels.routing import route_class
from api.bindings import MessageBinding

class APIDemultiplexer(WebsocketDemultiplexer):

    consumers = {
      'questions': MessageBinding.consumer
    }

channel_routing = {
    'websocket.connect': consumers.ws_connect,
    'websocket.receive': consumers.ws_receive,
    'websocket.disconnect': consumers.ws_disconnect,
}
