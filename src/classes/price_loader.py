import ccxt
from .callback import Callback
import asyncio

class PriceLoader(Callback):

    currencies      = None
    base_currencies = None
    exchanges       = {}
    logger          = None
    sleep_time      = None

    def __init__(self, currencies, base_currencies, logger=None, sleep_time=60000):
        super().__init__("KafkaCallback", logger=logger)
        self.currencies = currencies
        self.base_currencies = base_currencies
        self.sleep_time = int(sleep_time)/1000

    async def run(self):
        while True:
            tick = {}
            for pair, exchange in self._settings()["default_pairs"].items():
                tick[pair] = await self._get_tick_from_exchange(exchange, pair, self._settings()["timeout_between_request_s"])
                tick, _ = self._fix_missing_pairs(tick)
            self.logger.info("got base tick = %s, going" % tick)

            for curr in self.currencies:
                pair = "%s/BTC" % curr
                if pair not in tick.keys() or not tick.get(pair, None):
                    tick[pair] = await self._get_tick_from_exchange(self._settings()["default_exchange"], pair, self._settings()["timeout_between_request_s"])

            tick, _ = self._fix_missing_pairs(tick)
            # second time for cross-exchange pairs
            tick, _ = self._fix_missing_pairs(tick)

            tick = self._cleanup_tick(tick)

            self.logger.info("got full tick = %s, going for sleep for %s sec" % (tick, self.sleep_time))
            await self.sendCallback(tick)
            await asyncio.sleep(self.sleep_time)

    def _cleanup_tick(self, tick):
        for p in list(tick.keys()):
            sp = p.split("/")
            # NOTE: cleanup all sh*t like BTC/BTC, XLM/XRP, USD/XML
            if sp[0] == sp[1] or sp[1] not in self.base_currencies or sp[0] in ["USD", "USDT"]:
                del tick[p]
        # NOTE: necessary for proper kafka callback topic mapping
        tick["type"] = "prices"
        return tick

    def _get_exchange(self, name):
        if not self.exchanges.get(name, None):
            self.logger.info("exchange %s is not initialized, going to initialize..." % name)
            e = eval("ccxt." + name)()
            self.exchanges[name] = e
        return self.exchanges[name]

    def _settings(self):
        return {
            "default_pairs": {
                "BTC/USD"  : "kraken",
                "BCH/BTC"  : "kraken",
                "ETH/BTC"  : "kraken",
                "BTC/USDT" : "binance",
                "USDT/USD" : "kraken",
            },
            "default_exchange"          : "binance",
            "timeout_between_request_s" : 1
        }


    async def _get_tick_from_exchange(self, exchange_name, currency_pair, timeout = 0):
        tick = None
        try:
            tick = self._get_exchange(exchange_name).fetch_ticker(currency_pair)["last"]
            self.logger.info("[{}]: got tick = {} for pair = {}".format(exchange_name, tick, currency_pair))

            if timeout != 0:
                self.logger.info("going for {}s timeout".format(timeout))
                await asyncio.sleep(timeout)
        except Exception as e:
            self.logger.exception("[{}]: got exception {}".format(exchange_name, e))
        return tick

    def _get_price_for(self, tick, amount, currency1, currency2):
        pair     = "%s/%s" % (currency1, currency2)
        reversed = "%s/%s" % (currency2, currency1)

        try:
            if pair in tick.keys() and tick[pair] != -1:
                return amount * tick[pair]
            if reversed in tick.keys() and tick[reversed] != -1:
                return amount / tick[reversed]

            btc_a = currency1 + "/BTC"
            btc_b = "BTC/" + currency2

            return amount * tick[btc_a] * tick[btc_b]
        except Exception as e:
            self.logger.exception("error while _get_price_for(%s, %s, %s, %s)" % (tick, amount, currency1, currency2))
            return -1

    def _fix_missing_pairs(self, tick):
        #print "tick before = " + str(tick)
        currencies = []
        pairs      = []
        for pair, price in tick.items():
            if "/" in pair:
                for curr in pair.split("/"):
                    if curr not in currencies:
                        currencies.append(curr)

        changes = {}
        for curr1 in currencies:
            for curr2 in currencies:
                new_pair = "{}/{}".format(curr1, curr2)
                if curr1 != curr2:
                    if new_pair not in pairs:
                        pairs.append(new_pair)

                    if new_pair not in tick.keys() or tick[new_pair] == -1:
                        changes[new_pair] = self._get_price_for(tick, 1, curr1, curr2)
                        tick[new_pair]    = changes[new_pair]
                else:
                    if new_pair not in tick.keys():
                        tick[new_pair] = 1
        return tick, changes
