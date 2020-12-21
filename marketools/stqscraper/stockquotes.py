from . import get_dwl_storage_status, get_dwl_storage_dir
import pandas as pd
import numpy as np
from os import path
from urllib.request import urlretrieve
from datetime import datetime, timedelta


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
    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self._historical_ohlc = None

    @property
    def data(self):
        if self._historical_ohlc is None:
            self._historical_ohlc = self._get_data()
        return self._historical_ohlc

    @property
    def csv_file_path(self):
        if get_dwl_storage_status():
            output = path.join(get_dwl_storage_dir(), f'{self.ticker}_ohcl.csv')
        else:
            output = None
        return output

    def download_ohlc_from_stooq(self):
        url = f'http://stooq.com/q/d/l/?i=d&s={self.ticker}'
        file_path, _ = urlretrieve(url)
        try:
            output = read_ohlcv_from_csv(file_path)
        except ValueError:  # Stooq: Exceeded the daily hits limit
            output = None
        return output

    def _get_data(self):
        update_required = True  # assuming that update will be required
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
        if get_dwl_storage_status() and path.exists(self.csv_file_path):
            timestamp_now = datetime.timestamp(time_now)
            timestamp_up = path.getatime(self.csv_file_path)  # CSV file modification time

            # CSV updated within last 24 hours or it is weekend (no new data) 
            if (timestamp_now - timestamp_up < 24 * 3600) or is_weekend:
                output = read_ohlcv_from_csv(self.csv_file_path)
                last_ohlc_time = output.iloc[-1].name

                if last_ohlc_time.date() == expected_ohlc_time.date() or (time_now.hour < 20 and not is_weekend):
                    update_required = False

        if update_required:
            # update CSV file and read data 
            new_output = self.download_ohlc_from_stooq()

            if not new_output.empty:
                # Updated data downloaded - update output
                output = new_output
                # save to CSV
                if get_dwl_storage_status():
                    new_output.to_csv(self.csv_file_path)
            else:
                # Update error (Stooq: Exceeded the daily hits limit) 
                pass
    
        if not output.empty:
            output.sort_index(ascending=True, inplace=True)
        
        return output


if __name__ == '__main__':
    pass
