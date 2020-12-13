import requests
import pandas as pd
import re


def get_raw_summary_table(ticker):
    """
    Downloads and returns raw summary table from Stooq.

    Parameters
    ----------
    ticker : str
        ticker of a stock
    Returns
    -------
    pd.DataFrame
    """

    url = f'https://stooq.pl/q/g/?s={ticker}'
    html = requests.get(url).text

    # extracting table with summary
    raw_table = pd.read_html(html)[0]
    idx = raw_table.iloc[:, 0]
    raw_table.set_index(idx, inplace=True)

    return raw_table


def scrap_summary_table(ticker):
    """
    Scraps summary table with information about given stock ticker. Returns 
    dictionary with keys: Las - last price, Open - last open price, Volume - 
    last volume, EPS - EPS, P/E - P/E, P/BV - P/BV, Dividend yield % - dividend
    yield in percents. 

    Parameters
    ----------
    ticker : str
        ticker of a stock
    Returns
    -------
    dict
    """

    # get raw table    
    raw_table = get_raw_summary_table(ticker)

    # Stooq is Polish - translations needed
    keys = {
        'Last': 'Kurs',
        'Open': 'Otwarcie',
        'Volume': 'Wolumen',
        'EPS': 'EPS (ttm)',
        'P/E': 'C/Z (ttm)',
        'P/BV': 'C/WK',
        'Dividend yield %': 'Stopa dywidendy'
    }

    # creating and filling output dict 
    output_dict = dict()
    for k in keys:
        try:
            output_dict[k] = raw_table.loc[keys[k], 1]
        except KeyError:
            output_dict[k] = None

    # remove currency from price using regex
    m = re.search(r'\d+(\.\d+)?', output_dict['Last'])
    output_dict['Last'] = m.group(0)

    # remove % from dividend yield
    if output_dict['Dividend yield %']:
        output_dict['Dividend yield %'] = output_dict['Dividend yield %'][:-1] 

    for k in output_dict.keys():
        if output_dict[k]:
            output_dict[k] = float(output_dict[k])

    return output_dict


if __name__ == '__main__':
    pass
