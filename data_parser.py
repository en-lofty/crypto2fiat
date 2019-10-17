from time import time
from typing import Union

from coinmarketcap import Market

from config import *


class DataParser:
    coinmarketcap = Market()
    _data: dict
    _coin_ids: dict

    def __init__(self, no_cache=False) -> None:
        super().__init__()
        self._generate_ids()
        self.no_cache = no_cache
        self._data = dirs.load("data") if dirs.exists("data") else None
        logger.debug("DataParser initialized")

    def _get_id(self, coin_name: str) -> Union[int, None]:
        """
        Get the id of a coin via its name
        """

        # find the element with `coin_name` as a value
        logger.debug(f"Grabbing {coin_name} id...")

        for k, v in self._coin_ids.items():
            if coin_name in v.values() or coin_name == v.get("symbol"):
                return v.get("id")

    @property
    def data(self):
        # first check to see if data exists and is still within valid time frame
        if not self.use_existing_data or self.no_cache:
            logger.info("Downloading coin data from CoinMarketCap server...")
            response = self.coinmarketcap.ticker()
            if "data" not in response:
                logger.error("Unable to retrieve data from server")
                exit(-1)
            dirs.save("data", response["data"])
            logger.debug("Updating save time")
            dirs.save("metadata", dict(last_save_time=int(round(time() * 1000))))
            self._data = response["data"]
        return self._data or dirs.load("data")

    def _get_ticker(self, coin: str, fiat: str) -> Union[dict, None]:
        """
        Grab the coin information from the CoinMarketCap servers
        """
        logger.info(f"Grabbing {coin} ticker...")
        coin_id = self._get_id(coin)
        if str(coin_id) not in self.data:
            exit(f"'{coin}' not recognized.")
        ticker = self.data[str(coin_id)]

        if fiat not in ticker["quotes"]:
            new_ticker = self.coinmarketcap.ticker(str(coin_id), convert=fiat)["data"]
            if not isinstance(new_ticker, dict):
                logger.error(f"Expected dict, received {type(new_ticker)}")
                exit("An unknown error occurred.")
            # save new ticker information to existing data
            self._data[str(coin_id)]["quotes"].update(new_ticker["quotes"])
            dirs.save("data", self._data)
            return new_ticker
        return self.data[str(coin_id)]
        # check last coin data save date

    @property
    def use_existing_data(self) -> bool:
        """
        Check to see if data needs to be refreshed
        """
        # does previous coin data exist?
        if not dirs.exists("data") or not dirs.exists("metadata"):
            return False

        # if that last save date is greater then the allowed time, re-download data
        last_check_time = dirs.load("metadata")["last_save_time"]

        # was the last time we checked less than 30 minutes ago?
        return int(round(time() * 1000)) - last_check_time < settings.CACHE_REFRESH_TIME * (1000 * 60)

    def _get_fiat_price(self, fiat: str, coin: str) -> float:
        """
        Get the value in fiat for 1 coin
        """
        quotes = self._get_ticker(coin, fiat).get("quotes")
        if fiat not in quotes:
            exit("The fiat currency you entered is unrecognized. "
                 "Use --help to see available currencies.")
        return float(quotes[fiat]["price"])

    def convert_to_fiat(self, fiat: str, coin: str, amount: float) -> float:
        """
        Convert the given coin to the equivalent fiat amount
        """
        logger.debug('Converting %s %s to %s...', amount, coin, fiat)
        price = self._get_fiat_price(fiat, coin)
        return float(amount * price)

    def convert_to_crypto(self, fiat: str, coin: str, amount: float):
        """
        Take a usd amount and find the crypto coin equivalent
        """
        logger.debug('Converting %s %s to %s...', amount, fiat, coin)
        price = self._get_fiat_price(fiat, coin)
        return float(amount / price)

    def _generate_ids(self):
        if dirs.exists("ids"):
            self._coin_ids = dirs.load("ids")
            return

        # grab all the data
        logger.info("Downloading coin ids")
        coin_data = self.coinmarketcap.listings()  # type: dict
        logger.debug(f"Attempting to save coin ids...")

        # get each coins data and grab the id and name
        data = {d["symbol"]: {"id": d["id"], "name": d["name"].upper(), "symbol": d["symbol"].upper()} for d in
                coin_data.get("data")}
        dirs.save("ids", data)
        self._coin_ids = data
