from .stqscraper import DATA_DIR
from .stqscraper.fundamentals import Fundamentals
from .stqscraper.stockquotes import StockQuotes
from .stqscraper.scrapers import scrap_summary_table
import pandas as pd
import os


class Stock:
    """
    Class representing a stock with given ticker.

    Attributes
    ----------
    ticker : str
        ticker of a stock; country code needs to be append after a dot for not
        Polish stocks, e.g, 'AAPL.US'
    ohlc : pandas.DataFrame
        DataFrame with OHLC prices (open-high-low-close), and volume
    fundamentals : dict
        dictionary with available fundamental information
    """

    def __init__(self, ticker: str):
        self.ticker = ticker
        self._ohlc = StockQuotes(ticker)
        self._fundamentals = Fundamentals(ticker)

    # @property
    # def name(self):
    #     stocks = dict()
    #     return stocks.get(self.ticker, None)

    @property
    def ohlc(self):
        """
        Returns DataFrame with OHLC prices (open-high-low-close), and volume.
        """
        return self._ohlc.data

    @property
    def last_ohlc(self):
        """
        Returns the most recent OHLC prices (open-high-low-close), and volume.
        """
        return self.ohlc.iloc[-1]

    @property
    def price(self):
        """Returns last price."""
        return scrap_summary_table(self.ticker)['Last']

    @property
    def volume(self):
        """Returns last volume."""
        return scrap_summary_table(self.ticker)['Volume']

    @property
    def fundamentals(self):
        """Returns fundamental information, if available."""
        if not bool(self._fundamentals):
            self._fundamentals.get_fundamentals()
        return self._fundamentals

    @property
    def eps(self):
        """Returns earning per share, if available."""
        return self.fundamentals.get('EPS')

    @property
    def pe(self):
        """Returns price–earnings ratio, if available."""
        return self.fundamentals.get('P/E')

    @property
    def pbv(self):
        """Returns price–to-book ratio, if available."""
        return self.fundamentals.get('P/BV')

    @property
    def dividend_yield(self):
        """Returns dividend yield, if available."""
        return self.fundamentals.get('Dividend yield')

    @property
    def stooq_plot_link(self):
        """Returns link to Stooq page with HTML chart with OHLC data."""
        link = f'https://stooq.pl/q/a2/?s={self.ticker}'
        return link

    def mean_volume(self, window: int):
        """
        Returns mean volume over given number of the most recent sessions.

        Parameters
        ----------
        window : int
            number of recent stock market sessions the average should be 
            calculated over

        Returns
        -------
        float
        """
        volume = self.ohlc.tail(window)['Volume']
        output = volume.mean()
        return output


if __name__ == '__main__':
    pass
