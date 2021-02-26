import os


STORE_DWL_DATA = False
DWL_DATA_DIR = os.path.join(os.path.expanduser('~'), '.marketools_data')


def store_data():
    global STORE_DWL_DATA
    STORE_DWL_DATA = True
    if not os.path.exists(DWL_DATA_DIR):
        os.mkdir(DWL_DATA_DIR)


def get_storage_status():
    return STORE_DWL_DATA


def get_storage_dir():
    return DWL_DATA_DIR
