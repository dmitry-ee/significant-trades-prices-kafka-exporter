import argparse
import os
from .log import LOGGER
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--stpke_kafka_url",     help="url for kafka",                     type=str,   default=None)
parser.add_argument("--stpke_mongo_url",     help="url for mongodb",                   type=str,   default=None)
parser.add_argument("--stpke_default_db",    help="db for mongodb",                    type=str,   default="default")
parser.add_argument("--stpke_settings_collection", help="collection for settings",     type=str,   default="settings")
parser.add_argument("--stpke_prices_topic",  help="name of topic for price messages",  type=str,   default="prices")
parser.add_argument("--stpke_sleep_ms",      help="sleep timeout between requests",    type=int,   default=60000)


args = parser.parse_args()

SETTINGS = {}
for a, v in vars(args).items():
    SETTINGS[a] = v

#override with env values if needed
for k, v in SETTINGS.items():
    if k.upper() in os.environ:
        SETTINGS[k] = os.environ.get(k.upper())

LOGGER.warn("starting app with settings: %s" % SETTINGS )
