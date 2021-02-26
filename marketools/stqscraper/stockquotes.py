from . import get_storage_status, get_storage_dir
import pandas as pd
import numpy as np
from os import path
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import warnings


def read_ohlcv_from_csv(file_path):
    """
    Reads and returns OHLCV data from CSV file.

    Parameters
    ----------
    file_path : str or os.path
        path to CSV file with OHLCV data
    Returns
    -------
    pandas.DataFrame
    """
    
    output = pd.read_csv(file_path, 
                         index_col='Date',
                         parse_dates=['Date'],
                         date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d'))
    output['Volume'] = output['Volume'].astype(np.float64)
    return output


class StockQuotes:

    check_for_update = True  # if True OHLC data will be checked for updates
    update_period = 24  # time in hours, how often data are checked for updates
    update_hour = 20  # full hour after that the data are checked for update

    def __init__(self, ticker):
        self.ticker = ticker
        self._historical_ohlc = dict(d=None, w=None, m=None, q=None, y=None)

    @property
    def data(self):
        warnings.warn('data is depracted, use ohlc_d instead',
                      DeprecationWarning)
        if self._historical_ohlc['d'] is None:
            self._historical_ohlc['d'] = self._get_data(interval='d')
        return self._historical_ohlc['d']

    def ohlc(self, interval='d'):
        if self._historical_ohlc[interval] is None:
            self._historical_ohlc[interval] = self._get_data(interval=interval)
        return self._historical_ohlc[interval]

    @property
    def ohlc_d(self):
        return self.ohlc(interval='d')

    @property
    def ohlc_w(self):
        return self.ohlc(interval='w')

    @property
    def ohlc_m(self):
        return self.ohlc(interval='m')

    @property
    def ohlc_q(self):
        return self.ohlc(interval='q')

    @property
    def ohlc_y(self):
        return self.ohlc(interval='y')

    def csv_file_path(self, interval='d'):
        if get_storage_status():
            output = path.join(get_storage_dir(),
                               f'{self.ticker}_ohcl_{interval}.csv')
        else:
            output = None
        return output

    def download_ohlc_from_stooq(self, interval='d'):
        """
        Download CSV file with OHLC data from Stooq.com and reads the data into
        DataFrame. Returns None if daily hits limit for Stooq is exceeded.

        Parameters
        ----------
        interval : str
            single letter defining the interval for OHLC data:
            d - day (default), w - weekly, m - monthly, q - quarterly,
            y - yearly

        Returns
        -------
        pandas.DataFrame
        """
        url = f'http://stooq.com/q/d/l/?i={interval}&s={self.ticker}'
        file_path, _ = urlretrieve(url)
        try:
            output = read_ohlcv_from_csv(file_path)
        except ValueError:  # Stooq: Exceeded the daily hits limit
            output = None
        return output

    def _get_data(self, interval='d'):
        update_required = self.check_for_update  # assuming that update will be required
        output = pd.DataFrame()

        # time info 
        time_now = datetime.now()
        weekday_now = datetime.weekday(time_now)
        is_weekend = True if weekday_now in (5, 6) else False

        # calculate expected date for last OHLC data, consider only weekdays 
        # from Mo-Fr, assume that last update was one day earlier 
        delta_days = (weekday_now - 4) if is_weekend else 0
        expected_ohlc_time = time_now - timedelta(days=delta_days)

        # file with data for ticker exists
        if get_storage_status() and path.exists(self.csv_file_path(interval=interval)):
            timestamp_now = datetime.timestamp(time_now)
            timestamp_up = path.getatime(self.csv_file_path(interval=interval))  # CSV file modification time

            # CSV updated within last 24 hours or it is weekend (no new data) 
            if (timestamp_now - timestamp_up < StockQuotes.update_period * 3600) or is_weekend:
                output = read_ohlcv_from_csv(self.csv_file_path(interval=interval))
                last_ohlc_time = output.iloc[-1].name

                updated_data = last_ohlc_time.date() == expected_ohlc_time.date()
                session_time = time_now.hour < StockQuotes.update_hour and not is_weekend
                if updated_data or session_time:
                    update_required = False

        if update_required:
            # update CSV file and read data 
            new_output = self.download_ohlc_from_stooq(interval=interval)

            if not new_output.empty:
                # Updated data downloaded - update output
                output = new_output
                # save to CSV
                if get_storage_status():
                    new_output.to_csv(self.csv_file_path(interval=interval))
            else:
                # Update error (Stooq: Exceeded the daily hits limit) 
                pass
    
        if not output.empty:
            output.sort_index(ascending=True, inplace=True)
        
        return output


if __name__ == '__main__':
    pass
