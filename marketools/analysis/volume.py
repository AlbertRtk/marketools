

def mean_volume_on_date(volume_data, 
                        day, 
                        over_last=90):
    """
    Returns mean volume over given number of sessions before given date 
    (inclusively).

    Parameters
    ----------
    volume_data : pandas.DataFrame
        DataFrame with 'Volume' column
    day : date 
        date the mean volume should be calculated for
    over_last : int
        number of stock market sessions the average should be calculated over

    Returns
    -------
    float
    """
    
    volume = volume_data[:day].tail(over_last)['Volume']
    output = volume.mean()
    return output
