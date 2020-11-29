def print_red(skk): 
    print("\033[91m{}\033[00m" .format(skk)) 


def print_green(skk): 
    print("\033[92m{}\033[00m" .format(skk)) 


def determine_print_color_from_prices(price, purchase_price):
    print_color = print_green if price > purchase_price else print_red
    return print_color


def info_str(day, action, ticker, volume, price):
    return f'{day}: {action:<{2}} {ticker} \t {volume:>{4}} \t for {round(price, 2)}'
