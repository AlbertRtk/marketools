import pandas as pd


def macd(prices: pd.DataFrame, mid_const: int=12, long_const: int=26, signal_const: int=9):
    """
    Returns Pandas Dataframe with MACD, Signal, and Histogram.

    :param prices:
    :param mid_const:
    :param long_const:
    :param signal_const:
    :returns:
    """
    price = prices['Close']
    output = pd.DataFrame(columns=['MACD', 'Signal', 'Histogram'])

    # calculate MACD line = price.emw(12) - price.emw(26)
    ewm_mid = price.ewm(span=mid_const).mean()
    ewm_long = price.ewm(span=long_const).mean()
    output['MACD'] = ewm_mid - ewm_long

    # calculate signal line = MACD.emw(9)
    output['Signal'] = output['MACD'].ewm(span=signal_const).mean()

    # calculate histogram = MACD - signal
    output['Histogram'] = output['MACD'] - output['Signal']
    
    return output


if __name__=='__main__':
    pass
