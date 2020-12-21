import pandas as pd
import numpy as np


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

    output.loc[ohlc.index[0], 'Open'] = ohlc.loc[ohlc.index[0], 'Open']
    next_open = None
    for idx, val in output.iterrows():
        if next_open is not None:
            val['Open'] = next_open
            output.loc[idx, 'Open'] = next_open
        next_open = (val['Open'] + val['Close']) / 2

    output['High'] = ohlc['High']
    output['High'] = output[['High', 'Open', 'Close']].max(axis=1)

    output['Low'] = ohlc['Low']
    output['Low'] = output[['Low', 'Open', 'Close']].min(axis=1)

    output = output.astype(np.float64)

    return output
