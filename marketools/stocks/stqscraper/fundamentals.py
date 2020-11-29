from . import DATA_DIR
from datetime import datetime
import pandas as pd
import requests
import os
import csv


class Fundamentals(dict):
    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker

    def get_fundamentals(self):
        update_required = True  # assuming that update will be required
        file_path = os.path.join(DATA_DIR, f'{self.ticker}_indicators.csv')

        if os.path.exists(file_path):
            timestamp_now = datetime.timestamp(datetime.now())
            timestamp_up = os.path.getatime(file_path)  # CSV file modification time

            if timestamp_now - timestamp_up < 24 * 3600:
                """ do not update more often than once in 24 hours """
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    try:
                        self.update(next(reader))
                    except StopIteration:
                        pass
                update_required = False

        if update_required:
            """ data older than 24 hours - update """
            self.update(self._download_fundamentals())
            with open(file_path, 'w') as f:
                writer = csv.DictWriter(f, self.keys())
                writer.writeheader()
                writer.writerow(self)

        if bool(self) is False:
            """ no fundamental data (None or empty dict) """
            self.update()

    def _download_fundamentals(self):
        """
        Gets available on stooq.com stock fundamentals for ticker.

        :return: 
        """
        """ URL to web page with fundamentals """
        url = f'https://stooq.pl/q/g/?s={self.ticker}'
        html = requests.get(url).text

        """ extracting table with fundamentals and setting value names as index """
        raw_table = pd.read_html(html)[0]
        idx = raw_table.iloc[:, 0]
        raw_table.set_index(idx, inplace=True)

        """ using extract_fundamentals_from_table to pars data """
        return self._extract_fundamental_from_df_to_dict(raw_table)

    @staticmethod
    def _extract_fundamental_from_df_to_dict(table):
        """
        Extracts stock fundamentals from table (Pandas DataFrame) and return them in dict.

        :param table: Pandas DataFrame with data from raw html table
        :return:
        """
        """ names of fundamental values (keys) and polish translations (values) - stooq is polish """
        fund_val = {'EPS': 'EPS (ttm)',
                    'P/E': 'C/Z (ttm)',
                    'P/BV': 'C/WK',
                    'Dividend yield': 'Stopa dywidendy'}

        """ creating and filling output dict """
        output = dict()
        for k in fund_val.keys():
            try:
                output[k] = table.loc[fund_val[k], 1]
            except KeyError:
                pass

        return output


if __name__ == '__main__':
    pass
