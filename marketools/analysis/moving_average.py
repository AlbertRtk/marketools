import pandas as pd
import numpy as np


def simple_moving_average(ohlc: pd.DataFrame,
                          price: str = 'Close',
                          window: int = 15,
                          min_periods: int = 0):
    """
    Returns Pandas Series with the Simple Moving Average for the indicated price. NaN will be placed for days
    where there is not enough previous data (depends on min_periods)

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    price : str
        The price on which SMA will be calculated (Close by default)
    window : int
        Size of the moving window. This is the number of observations used for calculating the statistic
    min_periods: int
        Minimum number of observations in window required to have a value (otherwise result is NA)

    Returns
    -------
    pandas.Series
    """

    # implement simple moving average
    output = ohlc[price].rolling(window=window, min_periods=min_periods).mean()

    return output


def weighted_moving_average(ohlc: pd.DataFrame,
                            price: str = 'Close',
                            window: int = 15):
    """
    Returns Pandas Series with the Weighted Moving Average for the indicated price. NaN will be placed for days
    where there is not enough previous data

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    price : str
        The price on which WMA will be calculated (Close by default)
    window : int
        Size of the moving window. This is the number of observations used for calculating the statistic

    Returns
    -------
    pandas.Series
    """

    weights = np.arange(1, window + 1)

    # implement weighted moving average
    output = ohlc[price].rolling(window=window)\
        .apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)

    return output


def exponential_moving_average(ohlc: pd.DataFrame,
                               alpha: int,
                               price: str = 'Close'):
    """
    Returns Pandas Series with the Exponential Moving Average for the indicated price.

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    alpha : float
        smoothing factor, 0 < alpha <= 1
    price : str
        The price on which EMA will be calculated (Close by default)

    Returns
    -------
    pandas.Series
    """

    # implement exponential moving average
    output = ohlc[price].ewm(alpha=alpha, adjust=False).mean()

    return output


if __name__ == '__main__':
    pass
