from .client import Client, \
    CHANNEL_CREATE_TOPIC, CHANNEL_DESTROY_TOPIC
import re

class AtlasClient(Client):
    """MQTT client used to create and destroy Agent upon channel creation / destruction.

    This one is special.
    
    """

    def __init__(self):
        super(AtlasClient, self).__init__()

        self.on_create = self.handler_not_set
        self.on_destroy = self.handler_not_set

    def _get_client_id_and_operation(self, topic):
        r = re.search('atlas/(.*?)/channel/(.*)', topic)

        return (r.group(1), r.group(2))

    def on_connect(self, client, userdata, flags, rc):
        super(AtlasClient, self).on_connect(client, userdata, flags, rc)

        client.subscribe(CHANNEL_CREATE_TOPIC % '+')
        client.subscribe(CHANNEL_DESTROY_TOPIC % '+')

    def on_message(self, client, userdata, msg):
        id, op = self._get_client_id_and_operation(msg.topic)

        if op == 'create':
            self.on_create(id)
        elif op == 'destroy':
            self.on_destroy(id)