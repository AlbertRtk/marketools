

def mean_volume_on_date(volume_data, day, window=90):
    """
    Returns mean volume over given number of sessions before given date 
    (inclusively).

    Parameters
    ----------
    volume_data : pandas.DataFrame
        DataFrame with 'Volume' column
    day : date 
        date the mean volume should be calculated for
    window : int
        number of recent stock market sessions the average should be calculated 
        over

    Returns
    -------
    float
    """
    
    volume = volume_data[:day].tail(window)['Volume']
    output = volume.mean()
    
    return output


def select_stocks_with_increased_volume(stocks_dict: dict, long: int = 90, factor: float = 3.3) -> dict:

    """
    Returns dictionary with stocks (tickers as keys, Stock as values) that volume increased over a given factor compared
    to long average of volume (90 days by default).

    Parameters
    ----------
    stocks_dict : dict
        dictionary with tickers as keys and Stock as values
    long : int
        average window
    factor : float
        factor for minimum increase of volume

    Returns
    -------
    dict
    """
    selected = dict()

    for tck in stocks_dict.keys():
        stock = stocks_dict[tck]
        long_mean = stock.mean_volume(long)
        if (stock.volume/long_mean) > factor:
            selected[tck] = stock

    return selected
