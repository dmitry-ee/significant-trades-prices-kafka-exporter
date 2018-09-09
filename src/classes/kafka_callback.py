import websockets
import asyncio
import json
from .callback import Callback
from kafka import KafkaProducer
from kafka.errors import KafkaError

class KafkaCallback(Callback):

    kafka_url           = ""
    producer            = None
    type_topic_mapping  = None
    default_topic_name  = None
    default_retries     = None

    def __init__(self, kafka_url, logger=None, type_topic_mapping=[], default_topic_name="other", default_retries=3):
        super().__init__("KafkaCallback", logger=logger)

        self.kafka_url          = kafka_url
        self.type_topic_mapping = type_topic_mapping
        self.default_topic_name = default_topic_name
        self.default_retries    = default_retries

        self.init()

    def init(self):
        self.producer = KafkaProducer(
            bootstrap_servers=[self.kafka_url],
            value_serializer=lambda m: json.dumps(m).encode('ascii'),
            retries=3
        )

    async def processCallback(self, obj):
        #NOTE: awesome sh*t is going on here
        if type(obj) is str:
            obj = json.loads(obj)

        selected_topic = self.default_topic_name
        message_type = obj.get("type", None)
        if message_type and message_type in self.type_topic_mapping.keys():
            selected_topic = self.type_topic_mapping[message_type]

        if type(obj) != dict:
            raise Exception("object %s is not a dict!" % s)

        self.producer.send(selected_topic, obj).add_callback(self._kafka_log_success).add_errback(self._kafka_log_error)

    def _kafka_log_success(self, message):
        self.logger.info(message)

    def _kafka_log_error(self, message):
        self.logger.warning(message)
