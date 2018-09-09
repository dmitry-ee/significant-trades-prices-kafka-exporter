from .classes import MongoClient
from .settings import SETTINGS
from .log import LOGGER

if not SETTINGS["stpke_mongo_url"]:
    raise Exception("Mongo Url is not defined! App will exit...")

def init_base_settings():
    LOGGER.warning("db SETTINGS is empty, going to init...")
    default_settings = [
        { "name": "currencies", "value": [
            "BTC", "ETH", "XRP", "BCH", "EOS",
            "XLM", "LTC", "ADA", "XMR", "IOTA",
            "TRX", "NEO", "ETC"]
        },
        { "name": "base_currencies", "value": ["USD", "BTC", "ETH"] },
    ]
    for setting in default_settings:
        m.append("settings", { "_id": setting["name"], "value": setting["value"] })

m = MongoClient(SETTINGS["stpke_mongo_url"], SETTINGS["stpke_default_db"])
currencies      = m.find_one("settings", { "_id":"currencies" })
base_currencies = m.find_one("settings", { "_id":"base_currencies" })
if not currencies or not base_currencies:
    init_base_settings()
    currencies      = m.find_one("settings", { "_id":"currencies" })
    base_currencies = m.find_one("settings", { "_id":"base_currencies" })

CURRENCIES = currencies["value"]
BASE_CURRENCIES = base_currencies["value"]

LOGGER.warning("found currencies settings: %s" % CURRENCIES)
LOGGER.warning("found base_currencies settings: %s" % BASE_CURRENCIES)
