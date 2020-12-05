import pandas as pd


def rsi(prices: pd.DataFrame, window: int = 14):
    """
    Calculates Relative Strength Index (RSI).

    Parameters
    ----------
    prices : pandas.DataFrame 
        DataFrame with 'Close' column containing closing prices of stock
    window : int
        size of the moving window.

    Returns
    -------
    pandas.DataFrame
    """
    
    price_now = prices['Close']
    price_prev = prices['Close'].shift(periods=1, fill_value=0)  # assign to each day price from the previous day

    price_changes = pd.DataFrame(columns=['Up', 'Down'])
    price_changes['Up'] = price_now - price_prev  # upward changes
    price_changes['Down'] = price_prev - price_now  # downward changes
    price_changes[price_changes < 0] = 0

    smma = price_changes.ewm(span=window, adjust=False).mean()  # smoothed moving averages
    rs = smma['Up'] / smma['Down']

    output_rsi = -100 / (rs+1)
    output_rsi = output_rsi + 100

    output_rsi = output_rsi.rename('RSI')
    output_rsi = output_rsi.to_frame()

    return output_rsi


def rsi_cross_signals(rsi_values: pd.DataFrame, 
                      cross_line: float, 
                      direction: str='rise'):
    """
    Calculates buy/sell signals for given RSI signal line. Returns table with 
    True values for days when signal appears.

    Parameters
    ----------
    rsi_values : pandas.DataFrame 
        DataFrame with RSI column
    cross_line : float
        signal threshold line, when signal line crosses this line signal is set
    direction : str
        direction the signal line should cross threshold line 
        ('rise' - signal increasing [default], 'fall' - signal decreasing)
    
    Returns
    -------
    pandas.DataFrame
    """

    if not (0 < cross_line < 100):
        raise ValueError('cross_line takes values from 0 to 100')

    rsi_copy = pd.DataFrame()
    rsi_copy['RSI'] = rsi_values['RSI']
    rsi_copy['RSI day before'] = rsi_values['RSI'].shift(1)

    if 'rise' == direction:
        # True signal if RSI is increasing and crossing the threshold line
        output = (rsi_copy['RSI'] >= cross_line ) & (rsi_copy['RSI day before'] < cross_line)
    elif 'fall' == direction:
        # True signal if RSI is decreasing and crossing the threshold line
        output = (rsi_copy['RSI'] <= cross_line ) & (rsi_copy['RSI day before'] > cross_line)
    else:
        raise ValueError('wrong value for direction, must be "rise" or "fall"')

    return output
