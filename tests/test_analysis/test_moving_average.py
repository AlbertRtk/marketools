import pytest
from marketools.analysis.moving_average import simple_moving_average, weighted_moving_average, exponential_moving_average
import pandas as pd
import numpy as np


@pytest.fixture
def NineDayPrices():
    prices = np.array([3.37, 4.21, 4.10, 3.90, 3.79, 3.76, 3.65, 3.75, 3.88])
    df = pd.DataFrame(prices, columns=['Close'])
    return df


@pytest.mark.parametrize("window,expected", [
    (2, np.array([3.79, 4.155, 4.00, 3.845, 3.775, 3.705, 3.70, 3.815])),
    (3, np.array([3.89, 4.07, 3.93, 3.82, 3.73, 3.72, 3.76]))
])
def test_simple_moving_average(NineDayPrices, window, expected):
    output = simple_moving_average(NineDayPrices, window=window)
    output.dropna(inplace=True)
    output_arr = output.to_numpy()

    for i in range(len(expected)):
        assert pytest.approx(expected[i], output_arr[i])

    assert len(expected) == len(output_arr)


@pytest.mark.parametrize("window,expected", [
    (2, np.array([3.93, 4.1367, 3.967, 3.83, 3.77, 3.687, 3.72, 3.84])),
    (3, np.array([4.015, 4.018, 3.88, 3.79, 3.71, 3.718, 3.798])),
])
def test_weighted_moving_average(NineDayPrices, window, expected):
    output = weighted_moving_average(NineDayPrices, window=window)
    output.dropna(inplace=True)
    output_arr = output.to_numpy()

    for i in range(len(expected)):
        assert pytest.approx(expected[i], output_arr[i])

    assert len(expected) == len(output_arr)


@pytest.mark.parametrize("span,expected", [
    (2, np.array([3.37, 3.93, 4.043333333, 3.947777778, 3.842592593, 3.787530864, 3.695843621, 3.731947874, 3.830649291])),
    (3, np.array([3.37, 3.79, 3.945, 3.9225, 3.85625, 3.808125, 3.7290625, 3.73953125, 3.809765625])),
])
def test_exponential_moving_average(NineDayPrices, span, expected):
    output = exponential_moving_average(NineDayPrices, window=span)
    output.dropna(inplace=True)
    output_arr = output.to_numpy()

    for i in range(len(expected)):
        assert pytest.approx(expected[i], output_arr[i])

    assert len(expected) == len(output_arr)
