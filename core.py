#!/home/raphael/.local/share/virtualenvs/python-O_96yZmr/bin/python
import time

import click
import logzero
import pyperclip
import sh

from config import *
from data_parser import DataParser


# todo add logging to log directory

@click.command()
@click.argument('coin')
@click.argument('fiat')
@click.argument('amount', type=float)
@click.option('--reverse', "-r", multiple=True, is_flag=True, default=False, help="Fiat to cryptocurrency")
@click.option('--clipboard', '-c', multiple=True, is_flag=True, default=False, help="Copy the result to the clipboard")
@click.option('--verbose', '-v', multiple=True, is_flag=True, default=False)
@click.option('--timer', '-t', multiple=True, is_flag=True, default=False)
@click.option('--wordform', '-w', multiple=True, is_flag=True, default=False,
              help="Say the command in plain words for clarity")
def core(coin: str, fiat: str, amount: float, reverse: bool, clipboard: bool, verbose: bool, timer, wordform):
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
    t1 = time.time()
    if verbose:
        logzero.loglevel(logging.DEBUG)

    data_parser = DataParser()
    fiat = fiat.upper()
    coin = coin.upper()

    if reverse:
        logger.debug(f"Converting {amount} {fiat} to {coin}")
        if wordform:
            click.echo(f"What is ${amount:.2f} {fiat} worth in {coin}?")
        quantity = data_parser.convert_to_crypto(fiat.upper(), coin.upper(), amount)
        print("{:.8f}".format(quantity))
    else:
        logger.debug(f"Converting {amount} {coin} to {fiat}")
        if wordform:
            click.echo(f"How much is {amount} {coin} in {fiat}?")
        quantity = data_parser.convert_to_fiat(fiat.upper(), coin.upper(), amount)
        print("{:,.2f}".format(quantity))

    if clipboard:
        pyperclip.copy(str(quantity))
        sh.notify_send("crypto2fiat", f"{quantity} copied to clipboard")
    t2 = time.time()
    if timer:
        print(f"Time elapsed: {t2 - t1:.3f} seconds")
    logger.debug(f"Main time elapsed: {t2 - t1:.3f} seconds")
    logger.debug("_____________________________________\n")


if __name__ == '__main__':
    core()
