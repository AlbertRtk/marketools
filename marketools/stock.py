from .stqscraper.fundamentals import Fundamentals
from .stqscraper.stockquotes import StockQuotes
from .stqscraper.scrapers import scrap_summary_table
from .analysis import heikinashi
from .__storage import get_storage_dir, get_storage_status
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
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
    def last(self):
        """Returns last price."""
        return scrap_summary_table(self.ticker)['Last']

    @property
    def open(self):
        """Returns last open price."""
        return scrap_summary_table(self.ticker)['Open']

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

    def heikinashi(self):
        # read from file
        file_path = os.path.join(get_storage_dir(), f'{self.ticker}_heikinashi.csv')
        use_storage = get_storage_status()

        if use_storage and os.path.exists(file_path):
            # read csv
            output = pd.read_csv(file_path,
                                 index_col='Date',
                                 parse_dates=['Date'],
                                 date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d'))
            output = output.astype(np.float64)

            # check is update needed
            last_ohlc_date = self.ohlc.index[-1]
            last_ha_date = output.index[-1]

            if last_ohlc_date > last_ha_date:
                first_open = (output.loc[last_ha_date, 'Open']
                              + output.loc[last_ha_date, 'Close']) / 2
                new_ha = heikinashi(self.ohlc[last_ha_date+timedelta(days=1):],
                                    first_open=first_open)
                output = pd.concat([output, new_ha])
                output.to_csv(file_path)
        else:
            # calculate Heikin-Ashi
            output = heikinashi(self.ohlc)

            if use_storage:
                output.to_csv(file_path)

        return output


if __name__ == '__main__':
    pass
