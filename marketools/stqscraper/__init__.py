import os


STORE_DWL_DATA = False
DWL_DATA_DIR = os.path.join(os.path.expanduser('~'), '.marketools_data')


def store_data():
    """
    By default scraped/downloaded data are not stored.
    This function enables data storage on local machine.
    """
    global STORE_DWL_DATA
    STORE_DWL_DATA = True
    if not os.path.exists(DWL_DATA_DIR):
        os.mkdir(DWL_DATA_DIR)


def get_storage_status():
    """Returns True is data storage is active."""
    return STORE_DWL_DATA


def get_storage_dir():
    """Returns storage directory."""
    return DWL_DATA_DIR
