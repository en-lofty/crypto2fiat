#!/home/raphael/.local/share/virtualenvs/crypto2fiat-zkZtR6RQ/bin/python

import click
import logzero
import pyperclip
import sh
from my_utils import util_setup, MeasureBlockTime

from config import *
from data_parser import DataParser


@click.command()
@click.argument('coin')
@click.argument('fiat')
@click.argument('amount', type=float, default=1)
@click.option('--reverse', "-r", multiple=True, is_flag=True, default=False, help="Fiat to cryptocurrency")
@click.option('--clipboard', '-c', multiple=True, is_flag=True, default=False, help="Copy the result to the clipboard")
@click.option('--verbose', '-v', multiple=True, is_flag=True, default=False)
@click.option('--timer', '-t', multiple=True, is_flag=True, default=False)
@click.option('--wordform', '-w', multiple=True, is_flag=True, default=False,
              help="Prints the command in plain words for clarity")
@click.option('--no-cache', is_flag=True, default=False,
              help=f"Do not use cached data. Price data is cached for {settings.CACHE_REFRESH_TIME} minutes")
def core(coin: str, fiat: str, amount: float, reverse: bool, clipboard: bool, verbose: bool, timer: bool,
         wordform: bool, no_cache: bool):
    """
    Converts a cryptocurrency amount to a fiat equivalent or vice-versa

    Valid fiat currency values are: "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
    "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY", "KRW", "MXN","MYR", "NOK",
    "NZD", "PHP", "PKR", "PLN", "RUB", "SEK", "SGD", "THB", "TRY","TWD", "ZAR"
    Valid cryptocurrency values are: "BTC", "ETH" "XRP", "LTC", and "BCH"

    `c2f btc usd 50`
    Translates to: What is 50 BTC worth in USD?

    `c2f btc usd 50 --reverse`
    Translates to: What is $50 USD worth in BTC?
    """
    util_setup(logger, timer, enabled_=True)
    with MeasureBlockTime("Main block"):
        if verbose:
            logzero.loglevel(logging.DEBUG)

        data_parser = DataParser(no_cache=no_cache)
        fiat = fiat.upper()
        coin = coin.upper()

        try:
            if reverse:
                if wordform:
                    click.echo(f"What is ${amount:.2f} {fiat} worth in {coin}?")
                quantity = data_parser.convert_to_crypto(fiat.upper(), coin.upper(), amount)
                formatted_quantity = "{:.8f}".format(quantity)

                print(formatted_quantity)
            else:
                if wordform:
                    click.echo(f"How much is {amount} {coin} in {fiat}?")
                quantity = data_parser.convert_to_fiat(fiat.upper(), coin.upper(), amount)
                formatted_quantity = "{:,.2f}".format(quantity)
                print(formatted_quantity)

            if clipboard:
                pyperclip.copy(formatted_quantity)
                sh.notify_send(APP_NAME, f"{formatted_quantity} copied to clipboard")
        except Exception as e:
            logger.exception(e)


if __name__ == '__main__':
    core()
    logger.debug("_____________________________________\n")
