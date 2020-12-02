import pytest
from marketools.analysis.moving_average import simple_moving_average, weighted_moving_average
import pandas as pd
import numpy as np


@pytest.fixture
def NineDayPrices():
    prices = np.array([3.37, 4.21, 4.10, 3.90, 3.79, 3.76, 3.65, 3.75, 3.88])
    df = pd.DataFrame(prices, columns=['Close'])
    return df


@pytest.mark.parametrize("window,min_periods,expected", [
    (2, 2, np.array([3.79, 4.155, 4.00, 3.845, 3.775, 3.705, 3.70, 3.815])),
    (2, 0, np.array([3.37, 3.79, 4.155, 4.00, 3.845, 3.775, 3.705, 3.70, 3.815]))
])
def test_simple_moving_average(NineDayPrices, window, min_periods, expected):
    output = simple_moving_average(NineDayPrices, window=window, min_periods=min_periods)
    output.dropna(inplace=True)
    output_rows = np.array([])
    for index, row in output.iterrows():
        output_rows = np.append(output_rows, row['Close'])

    for i in range(len(expected)):
        assert pytest.approx(expected[i], output_rows[i])

    assert len(expected) == len(output_rows)


@pytest.mark.parametrize("window,expected", [
    (2, np.array([3.93, 4.1367, 3.967, 3.83, 3.77, 3.687, 3.72, 3.84])),
    (3, np.array([4.015, 4.018, 3.88, 3.79, 3.71, 3.718, 3.798])),
])
def test_weighted_moving_average(NineDayPrices, window, expected):
    output = weighted_moving_average(NineDayPrices, window=window)
    output.dropna(inplace=True)
    output_rows = np.array([])
    for index, row in output.iterrows():
        output_rows = np.append(output_rows, row['Close'])

    for i in range(len(expected)):
        assert pytest.approx(expected[i], output_rows[i])

    assert len(expected) == len(output_rows)
