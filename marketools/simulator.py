import math
import pandas as pd
from marketools.wallet import calculate_investment_value, Wallet
from marketools.extra_print import print_green, print_red, \
    determine_print_color_from_prices, info_str


def simulator(time_range: pd.DatetimeIndex,
              traded_stocks: dict, 
              wallet: Wallet, 
              max_positions: int = 5, 
              take_profit: float = 0.0, 
              stop_loss: float = 0.0, 
              auto_trading: bool = False):
    """
    This function returns decorator for a stock market strategy, that returns 
    change of wallet value over given time_range (in pandas.DataFrame)

    Parameters
    ----------
    time_range : pandas.DatetimeIndex
        an array with trading days only (no Saturdays, Sundays, holidays)
    traded_stocks : dict
        a dictionary with stocks.stock.Stock instances
    wallet : marketools.Wallet
        Wallet for trading 
    max_positions : int 
        maximum number of different stocks in the wallet
    take_profit : float
        if the price of a stock increases by this fraction, it will be sold;
        if equal 0 - take profit is deactivated (default)
    stop_loss : float
        if the price of a stock decreases by this fraction (comparing to the 
        purchase price), it will be sold; 
        if equal 0 - stop loss is deactivated (default)
    auto_trading : boolean
        if True selling immediately when stop loss / take profit is reached is 
        simulated

    Returns
    -------
    decorator that returns pandas.DataFrame
    """

    def strategy_wrapper(func):

        def simulation(*args, **kwargs):
            wallet_history = pd.DataFrame(columns=['Date', 'Wallet state'])
            stocks_to_buy = []
            stocks_to_sell = []

            for day in time_range:
                day_str = day.strftime('%Y-%m-%d')

                # Buy selected day before. Loop over list, order can be important here.
                # Strategy can sort relevant stocks - high priority first.
                for tck in stocks_to_buy:
                    if not wallet.get_volume_of_stocks(tck):
                        price = traded_stocks[tck].ohlc['Open'].get(day, None)
                        if price:
                            total = calculate_investment_value(wallet, max_positions)
                            total = total - wallet(total)  # needs some money to pay commission
                            volume = math.floor(total/price)
                            if volume > 0:
                                wallet.buy(tck, volume, price)
                                print(info_str(day_str, 'B', tck, volume, price))
                                # make sure to not sell it the same day
                                if tck in stocks_to_sell:
                                    stocks_to_sell.remove(tck)

                # Sell selected day before. List to set, we dont care here about the order.
                # Set will remove duplicates.
                for tck in set(stocks_to_sell):
                    if wallet.get_volume_of_stocks(tck):
                        price = traded_stocks[tck].ohlc['Open'].get(day, None)
                        if price: 
                            print_color = determine_print_color_from_prices(price, wallet.get_purchase_price_of_stocks(tck))
                            volume = wallet.sell_all(tck, price)
                            print_color(info_str(day_str, 'S', tck, volume, price))

                # call decorated function - strategy function
                stocks_to_buy, stocks_to_sell = func(day=day, traded_stocks=traded_stocks, *args, **kwargs)

                # if auto trading is active, check if price of any stock in the wallet crossed
                # take proffit or stop loss price; if yes then sell it immediately 
                if auto_trading:
                    for tck in wallet.list_stocks().copy():

                        price_max = traded_stocks[tck].ohlc['High'].get(day, None)
                        if price:
                            wallet.update_price(tck, price_max)
                        if wallet.change(tck) > take_profit:
                            price = wallet.get_purchase_price_of_stocks(tck) * (1+take_profit)  # selling it immediately
                            price = round(price, 2)
                            volume = wallet.sell_all(tck, price)
                            print_green(info_str(day_str, 'TP', tck, volume, price))
                            continue

                        price_min = traded_stocks[tck].ohlc['Low'].get(day, None)
                        if price:
                            wallet.update_price(tck, price_min)
                        if wallet.change(tck) < -stop_loss:
                            price = wallet.get_purchase_price_of_stocks(tck) * (1-stop_loss)  # selling it immediately
                            price = round(price, 2)
                            volume = wallet.sell_all(tck, price)
                            print_red(info_str(day_str, 'SL', tck, volume, price))
                            
                for tck in wallet.list_stocks():                        
                    # update the price to the closing price and calculate relative price change
                    ohlc = traded_stocks[tck].ohlc
                    price = ohlc['Close'].get(day, None)
                    if price:
                        wallet.update_price(tck, price)

                    # if auto trading is not active, then take profit / stop loss the next day
                    if not auto_trading:

                        # take profit the next day
                        if take_profit and wallet.change(tck) > take_profit:
                            stocks_to_sell.append(tck)

                        # stop loss the next day - price below purchase price
                        if stop_loss and wallet.change(tck) < -stop_loss:
                            stocks_to_sell.append(tck)

                # save history of the wallet
                wallet_history = wallet_history.append(
                    {'Date': day, 'Wallet state': wallet.total_value},
                    ignore_index=True
                    )
            
            return wallet_history

        return simulation

    return strategy_wrapper


if None:
    """
    This code should not be called - this is just a template function for tested strategy.
    """
    @simulator(TRADING_DAYS, stocks_data, MY_WALLET, TAKE_PROFIT, STOP_LOSS)
    def __strategy_template(arguments, *args, **kwargs):
        """
        :param arguments: any arguments needed for the strategy can be passed
        """
        day = kwargs['day']  # argument passed by decorator
        traded_stocks = kwargs['traded_stocks']  # argument passed by decorator
        stocks_to_buy = []
        stocks_to_sell = []

        """
        place for code that will fill in stocks_to_buy and stocks_to_sell sets with tickers
        """

        return stocks_to_buy, stocks_to_sell


if __name__ == '__main__':
    pass
