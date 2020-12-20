import pandas as pd


def heikinashi(ohlc: pd.DataFrame) -> pd.DataFrame:
    """
    Returns DataFrame with Heikin-Ashi calculated for given input OHLC values.

    Parameters
    ----------
    ohlc :pd.DataFrame
        DataFrame with OHLC data

    Returns
    -------
    pd.DataFrame
    """

    output = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close'])

    output['Close'] = ohlc[['Open', 'High', 'Low', 'Close']].mean(axis=1)

    output['Open'] = ohlc[['Open', 'Close']].mean(axis=1)
    output['Open'] = output['Open'].shift(periods=1)

    output['High'] = ohlc['High']
    output['High'] = output[['High', 'Open', 'Close']].max(axis=1)

    output['Low'] = ohlc['Low']
    output['Low'] = output[['Low', 'Open', 'Close']].min(axis=1)

    output = output.drop(output.index[0])

    return output
