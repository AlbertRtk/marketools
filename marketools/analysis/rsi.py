import pandas as pd


def rsi(prices: pd.DataFrame, alpha: float=1/14):
    """
    Clculates Relative Strength Index (RSI).

    :prices: pandas.DataFrame with 'Close' column containing closing prices of stock
    :alpha: smoothing factor, 0 < alpha <= 1
    :return: pandas.Series with calculated RSI
    """
    price_now = prices['Close']
    price_prev = prices['Close'].shift(periods=1, fill_value=0)  # assign to each day price from the previous day

    price_changes = pd.DataFrame(columns=['Up', 'Down'])
    price_changes['Up'] = price_now - price_prev  # upward changes
    price_changes['Down'] = price_prev - price_now  # downward changes
    price_changes[price_changes < 0] = 0

    smma = price_changes.ewm(alpha = alpha, adjust=False).mean()  # smoothed moving averages
    rs = smma['Up'] / smma['Down']

    output_rsi = -100 / (rs+1)
    output_rsi = output_rsi + 100

    output_rsi = output_rsi.rename('RSI')
    output_rsi = output_rsi.to_frame()

    return output_rsi


def rsi_cross_signals(rsi_values: pd.DataFrame, cross_line: float, direction: str='onrise'):
    """
    Calculates buy/sell signals for given RSI signal line.

    :rsi_values: pandas.DataFrame with RSI column
    :cross_line: signal threshold line, when signal line crosses this line signal is set
    :direction: direction the signal line should cross threshold line 
        ('onrise' - signal increasing [default], 'onfall' - signal decreasing)
    :return: pandas.Series with with True values for days when signal appears
    """
    if not (0 < cross_line < 100):
        raise ValueError('cross_line takes values from 0 to 100')

    rsi_copy = pd.DataFrame()
    rsi_copy['RSI'] = rsi_values['RSI']
    rsi_copy['RSI day before'] = rsi_values['RSI'].shift(1)

    if 'onrise' == direction:
        # True signal if RSI is increasing and crossing the threshold line
        output = (rsi_copy['RSI'] >= cross_line ) & (rsi_copy['RSI day before'] < cross_line)
    elif 'onfall' == direction:
        # True signal if RSI is decreasing and crossing the threshold line
        output = (rsi_copy['RSI'] <= cross_line ) & (rsi_copy['RSI day before'] > cross_line)
    else:
        raise ValueError('wrong value for direction, must be "onrise" or "onfall"')

    return output
