import os


STORE_DWL_DATA = False
DWL_DATA_DIR = os.path.join(os.getcwd(), '.marketools_data')


def store_scraped_data():
    global STORE_DWL_DATA
    STORE_DWL_DATA = True
    if not os.path.exists(DWL_DATA_DIR):
        os.mkdir(DWL_DATA_DIR)


def get_dwl_storage_status():
    return STORE_DWL_DATA


def get_dwl_storage_dir():
    return DWL_DATA_DIR
