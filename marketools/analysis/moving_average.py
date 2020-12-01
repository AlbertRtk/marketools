import pandas as pd
import numpy as np


def simple_moving_average(ohlc: pd.DataFrame,
                          config ={"Open": False, "High": False, "Low": False, "Close": True},
                          window: int = 10,
                          min_periods: int = 0,):
    """
    Returns Pandas Dataframe with the Moving Average for Open, High, Low, Close.

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    config: dict
        Dictionary that specifies on which aspects of OHLC moving average will be applied. True indicates the function
        apply Moving Average, False indicates to ignore.
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
    for col in config.keys():
        if config[col]:
            output[col] = ohlc[col].rolling(window=window, min_periods=min_periods).mean()

    return output


#def weighted_moving_average()

if __name__=='__main__':
    pass
