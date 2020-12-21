import os

from marketools.analysis.rsi import relative_strength_index as rsi
from marketools.analysis.rsi import rsi_cross_signals
from marketools.analysis.macd import macd
from marketools.analysis.moving_average import simple_moving_average as sma
from marketools.analysis.moving_average import weighted_moving_average as wma
from marketools.analysis.moving_average import exponential_moving_average as ema
from marketools.analysis.price import simple_relative_price_change, price_change
from marketools.analysis.volume import mean_volume_on_date
from marketools.analysis.heikinashi import heikinashi


relative_price_change = simple_relative_price_change


STORE_ANALYSIS_DATA = False
ANALYSIS_DATA_DIR = os.path.join(os.getcwd(), '.marketools_data')


def store_analysis_data():
    global STORE_ANALYSIS_DATA
    STORE_ANALYSIS_DATA = True
    if not os.path.exists(ANALYSIS_DATA_DIR):
        os.mkdir(ANALYSIS_DATA_DIR)


def get_analysis_storage_status():
    return STORE_ANALYSIS_DATA


def get_analysis_storage_dir():
    return ANALYSIS_DATA_DIR
