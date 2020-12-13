import requests
import pandas as pd


def scrap_summary_table(ticker):
    """
    """

    # URL to web page with data
    url = f'https://stooq.pl/q/g/?s={ticker}'
    html = requests.get(url).text

    # extracting table with summary
    raw_table = pd.read_html(html)[0]
    idx = raw_table.iloc[:, 0]
    raw_table.set_index(idx, inplace=True)

    return raw_table
