from .settings      import SETTINGS
from .log           import LOGGER
from .classes       import PrintCallback, KafkaCallback, PriceLoader
import asyncio
import functools

if not SETTINGS["stpke_kafka_url"]:
    raise Exception("Kafka Url is not defined! App will exit...")

#kafka = KafkaProducer()
topic_mapping = {
    SETTINGS["stpke_prices_type"] : SETTINGS["stpke_prices_topic"],
}

from .mongo import CURRENCIES, BASE_CURRENCIES

loader = PriceLoader(CURRENCIES, BASE_CURRENCIES, logger=LOGGER, sleep_time=SETTINGS["stpke_sleep_ms"])
# p = PrintCallback()
kafka = KafkaCallback(SETTINGS["stpke_kafka_url"],
    type_topic_mapping=topic_mapping,
    logger=LOGGER
)

loader.addCallback(kafka)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(loader.run())
