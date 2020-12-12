import pandas as pd


def simple_relative_price_change(new_price: float, ref_price: float):
    """
    Calculates and returns relative price change.

    Parameters
    ----------
    new_price : float
        new/current price
    ref_price : float
        reference price

    Returns
    -------
    float
    """
    
    assert ref_price > 0
    return (new_price - ref_price) / ref_price


def price_change(ohlc: pd.DataFrame, 
                 shift: int = 0,
                 relative: bool = False,
                 percent: bool = False):
    """
    Calculates price change based on given DataFrame with OHLC prices.

    Parameters
    ----------
    ohlc : pandas.DataFrame
        DataFrame with OHLC data
    shift : int
        default is zero - price change is calculated as change within one day 
        (Close-Open); if greater than zero, the change is calculated in relation 
        to close price "shift" days before (Close[today]-Close[today-shift]) 
    relative : bool
        if True calculates relative price change
    relative : bool
        if True returns relative price change expressed in percentage (relative 
        must be True)

    Returns
    -------
    pandas.Series
    """

    if shift:
        ref_price = ohlc['Close'].shift(shift)
        name_str = f'({shift}d)'
    else:
        ref_price = ohlc['Open']
        name_str = '(daily)'

    change = ohlc['Close'] - ref_price

    if relative:
        change = change / ref_price
        if percent:
            change = 100 * change
            name_str = '%Change ' + name_str
        else:
            name_str = 'Relative change ' + name_str
    else:
        name_str = 'Change ' + name_str

    change = change.rename(name_str)

    return change
