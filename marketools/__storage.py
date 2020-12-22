import os
from .stqscraper import store_scraped_data


STORE_DATA = False
DATA_DIR = os.path.join(os.getcwd(), '.marketools_data')


def __create_data_storage_dir():
    if not os.path.exists(DATA_DIR):
        os.mkdir(DATA_DIR)


def store_data():
    global STORE_DATA
    STORE_DATA = True
    store_scraped_data()
    __create_data_storage_dir()


def get_storage_status():
    return STORE_DATA


def get_storage_dir():
    return DATA_DIR
