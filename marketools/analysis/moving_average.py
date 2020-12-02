import pandas as pd
import numpy as np


def simple_moving_average(ohlc: pd.DataFrame,
                          config=["Close"],
                          window: int = 10,
                          min_periods: int = 0):
    """
    Returns Pandas Dataframe with the Simple Moving Average for Open, High, Low, Close. NaN will be placed for days
    where there is not enough previous data (depends on min_periods)

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    config: list
        List that specifies on which aspects of OHLC moving average will be applied.
    window : int
        Size of the moving window. This is the number of observations used for calculating the statistic
    min_periods: int
        Minimum number of observations in window required to have a value (otherwise result is NA)

    Returns
    -------
    pandas.DataFrame
    """

    output = pd.DataFrame()

    # implement moving average for the OHLC columns
    for col in config:
        output[col] = ohlc[col].rolling(window=window, min_periods=min_periods).mean()

    return output


def weighted_moving_average(ohlc: pd.DataFrame,
                            config=["Close"],
                            window: int = 10):
    """
    Returns Pandas Dataframe with the Weighted Moving Average for Open, High, Low, Close. NaN will be placed for days
    where there is not enough previous data

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    config: list
        List that specifies on which aspects of OHLC moving average will be applied.
    window : int
        Size of the moving window. This is the number of observations used for calculating the statistic

    Returns
    -------
    pandas.DataFrame
    """

    output = pd.DataFrame()
    weights = np.arange(1, window + 1)

    # implement moving average for the OHLC columns
    for col in config:
        output[col] = ohlc[col].rolling(window=window)\
            .apply(lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)

    return output


if __name__ == '__main__':
    pass
