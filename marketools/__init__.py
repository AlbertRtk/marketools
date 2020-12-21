from marketools.stock import *
from marketools.wallet import Wallet
from marketools.analysis import *
from marketools.stqscraper import store_scraped_data
import os


__pdoc__ = dict()
__pdoc__['wallet'] = False


STORE_DATA = False
DATA_DIR = os.path.join(os.getcwd(), '.marketools_data')


def create_data_storage_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)


def store_data():
    global STORE_DATA
    STORE_DATA = True
    store_scraped_data()
    create_data_storage_dir()
