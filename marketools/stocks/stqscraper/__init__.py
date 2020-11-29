import os


# DATA_DIR = os.path.join(os.path.expanduser('~'), '.stock_market_data')
DATA_DIR = os.path.join(os.getcwd(), '.stock_market_data')

if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)
