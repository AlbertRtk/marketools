from . import DATA_DIR
from datetime import datetime
import pandas as pd
import requests
import os
import csv
from .scrapers import scrap_summary_table


class Fundamentals(dict):
    """
    Class Fundamentals
    """

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker

    def get_fundamentals(self):
        """
        Scraps from Stooq.com fundamental information for given ticker.
        """

        update_required = True  # assuming that update will be required
        file_path = os.path.join(DATA_DIR, f'{self.ticker}_indicators.csv')

        if os.path.exists(file_path):
            timestamp_now = datetime.timestamp(datetime.now())
            timestamp_up = os.path.getatime(file_path)  # CSV file modification time

            if timestamp_now - timestamp_up < 24 * 3600:
                # do not update more often than once in 24 hours
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f)
                    try:
                        self.update(next(reader))
                    except StopIteration:
                        pass
                update_required = False
                # make sure that values are float
                for k in self.keys():
                    if self[k]:
                        self[k] = float(self[k])

        if update_required:
            # data older than 24 hours - update
            self.update(scrap_summary_table(self.ticker))
            with open(file_path, 'w') as f:
                writer = csv.DictWriter(f, self.keys())
                writer.writeheader()
                writer.writerow(self)

        if bool(self) is False:
            # no fundamental data (None or empty dict)
            self.update()

    
if __name__ == '__main__':
    pass
