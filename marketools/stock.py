from .stqscraper import DATA_DIR
from .stqscraper.fundamentals import Fundamentals
from .stqscraper.stockquotes import StockQuotes
import pandas as pd
import os


class Stock:
    def __init__(self, ticker):
        self.ticker = ticker
        self._ohlc = StockQuotes(ticker)
        self._fundamentals = Fundamentals(ticker)

    # @property
    # def name(self):
    #     stocks = dict()
    #     return stocks.get(self.ticker, None)

    @property
    def ohlc(self):
        return self._ohlc.data

    @property
    def last_ohlc(self):
        return self.ohlc.iloc[-1]

    @property
    def date(self):
        """ Returns date of last price """
        output = self.last_ohlc.name
        output = output.strftime('%Y-%m-%d')
        return output

    @property
    def price(self):
        """ Returns last price """
        return self.last_ohlc['Close']

    @property
    def volume(self):
        """ Returns last session volume"""
        return self.last_ohlc['Volume']

    @property
    def fundamentals(self):
        if not bool(self._fundamentals):
            self._fundamentals.get_fundamentals()
        return self._fundamentals

    @property
    def eps(self):
        output = self.fundamentals.get('EPS')
        if output is not None:
            output = float(output)
        return output

    @property
    def pe(self):
        output = self.fundamentals.get('P/E')
        if output is not None:
            output = float(output)
        return output

    @property
    def pbv(self):
        output = self.fundamentals.get('P/BV')
        if output is not None:
            output = float(output)
        return output

    @property
    def dividend_yield(self):
        output = self.fundamentals.get('Dividend yield')
        if output is not None:
            output = output[0:-1]
            output = float(output)
        return output

    @property
    def stooq_plot_link(self):
        link = f'https://stooq.pl/q/a2/?s={self.ticker}'
        return link

    def mean_volume(self, over_last):
        volume = self.ohlc.tail(over_last)['Volume']
        output = volume.mean()
        return output


if __name__ == '__main__':
    pass
