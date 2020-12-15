import math
import warnings
import pandas as pd
from marketools.wallet import calculate_investment_value, Wallet
from marketools.extra_print import print_green, print_red, \
    determine_print_color_from_prices, info_str


class Simulator:
    """
    Simulator for stock market strategies.

    Attributes
    ----------
    time_range : pandas.DatetimeIndex
        an array with trading days only (no Saturdays, Sundays, holidays)
    traded_stocks_data : dict
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
    live_trading : boolean
        if True selling immediately when stop loss / take profit is reached is
        simulated
    """

    def __init__(self, time_range: pd.DatetimeIndex, traded_stocks_data: dict,
                 wallet: Wallet, max_positions: int = 5,
                 take_profit: float = 0.0, stop_loss: float = 0.0,
                 live_trading: bool = False):

        self.time_range = time_range
        self.traded_stocks_data = traded_stocks_data
        self.wallet = wallet
        self.wallet_init_value = wallet.total_value
        self.max_positions = max_positions
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.live_trading = live_trading
        self.wallet_history = pd.DataFrame(columns=['Date', 'Wallet state'])

    def reset(self) -> None:
        """
        Resets the value of wallet to initial value, and removes all stocks from
        the wallet and its history.
        """
        self.wallet = Wallet(self.wallet.rate, self.wallet.minimum)
        self.wallet.money = self.wallet_init_value
        self.wallet_history = pd.DataFrame(columns=['Date', 'Wallet state'])

    def run(self, strategy_function, *args, **kwargs) -> pd.DataFrame:
        """
        Runs the simulation for given strategy and returns DataFrame with
        wallet value for each day in given time range.

        Parameters
        ----------
        strategy_function : func
            Function with investment strategy. Must take dictionary with traded
            stocks data (self.traded_stocks_data) and date as inputs. Must
            return set of lists (stocks_to_buy, stocks_to_sell).
        kwargs
            Other inputs to investment strategy (strategy_function).

        Returns
        -------
        pandas.DataFrame
        """

        stocks_to_buy = []
        stocks_to_sell = []

        for day in self.time_range:
            day_str = day.strftime('%Y-%m-%d')

            # Buy selected day before. Loop over list, order can be important
            # here. Strategy can sort relevant stocks - high priority first.
            for tck in stocks_to_buy:

                if not self.wallet.get_volume_of_stocks(tck):
                    price = self.traded_stocks_data[tck].ohlc['Open']\
                        .get(day, None)

                    if price:
                        total = calculate_investment_value(
                            self.wallet, self.max_positions)

                        # needs some money to pay commission
                        total = total - self.wallet.commission(total)
                        volume = math.floor(total / price)

                        if volume > 0:
                            self.wallet.buy(tck, volume, price)
                            print(info_str(day_str, 'B', tck, volume, price))
                            # make sure to not sell it the same day

                            if tck in stocks_to_sell:
                                stocks_to_sell.remove(tck)

            # Sell selected day before. List to set, we don't care here about
            # the order. Set will remove duplicates.
            for tck in set(stocks_to_sell):

                if self.wallet.get_volume_of_stocks(tck):
                    price = self.traded_stocks_data[tck].ohlc['Open']\
                        .get(day, None)

                    if price:
                        print_color = determine_print_color_from_prices(
                            price,
                            self.wallet.get_purchase_price_of_stocks(tck))
                        volume = self.wallet.sell_all(tck, price)
                        print_color(info_str(day_str, 'S', tck, volume, price))

            # call decorated function - strategy function
            stocks_to_buy, stocks_to_sell = strategy_function(
                day=day, traded_stocks=self.traded_stocks_data, *args, **kwargs)

            # if auto trading is active, check if price of any stock in the
            # wallet crossed take profit or stop loss price; if yes then sell it
            # immediately
            if self.live_trading:

                for tck in self.wallet.list_stocks().copy():
                    price_max = self.traded_stocks_data[tck].ohlc['High']\
                        .get(day, None)

                    if price_max:
                        self.wallet.update_price(tck, price_max)

                    if self.wallet.change(tck) > self.take_profit:
                        # selling it immediately
                        price = self.wallet.get_purchase_price_of_stocks(tck)\
                                * (1 + self.take_profit)
                        price = round(price, 2)
                        volume = self.wallet.sell_all(tck, price)
                        print_green(info_str(day_str, 'TP', tck, volume, price))
                        continue

                    price_min = self.traded_stocks_data[tck].ohlc['Low']\
                        .get(day, None)

                    if price_min:
                        self.wallet.update_price(tck, price_min)

                    if self.wallet.change(tck) < -self.stop_loss:
                        # selling it immediately
                        price = self.wallet.get_purchase_price_of_stocks(tck)\
                                * (1 - self.stop_loss)
                        price = round(price, 2)
                        volume = self.wallet.sell_all(tck, price)
                        print_red(info_str(day_str, 'SL', tck, volume, price))

            for tck in self.wallet.list_stocks():
                # update the price to the closing price
                ohlc = self.traded_stocks_data[tck].ohlc
                price = ohlc['Close'].get(day, None)

                if price:
                    self.wallet.update_price(tck, price)

                # if auto trading is not active, then take profit / stop loss
                # the next day
                if not self.live_trading:

                    # take profit the next day
                    if (self.take_profit > 0) \
                            and (self.wallet.change(tck) > self.take_profit):
                        stocks_to_sell.append(tck)

                    # stop loss the next day - price below purchase price
                    if (self.stop_loss > 0)\
                            and (self.wallet.change(tck) < -self.stop_loss):
                        stocks_to_sell.append(tck)

            # save history of the wallet
            self.wallet_history = self.wallet_history.append(
                {'Date': day, 'Wallet state': self.wallet.total_value},
                ignore_index=True)

        return self.wallet_history


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

    warnings.warn("deprecated, consider using Simulator class instead",
                  DeprecationWarning)

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


# if None:
#     """
#     This code should not be called - this is just a template function for tested strategy.
#     """
#     @simulator(TRADING_DAYS, stocks_data, MY_WALLET, TAKE_PROFIT, STOP_LOSS)
#     def __strategy_template(arguments, *args, **kwargs):
#         """
#         :param arguments: any arguments needed for the strategy can be passed
#         """
#         day = kwargs['day']  # argument passed by decorator
#         traded_stocks = kwargs['traded_stocks']  # argument passed by decorator
#         stocks_to_buy = []
#         stocks_to_sell = []
#
#         """
#         place for code that will fill in stocks_to_buy and stocks_to_sell sets with tickers
#         """
#
#         return stocks_to_buy, stocks_to_sell


if __name__ == '__main__':
    pass
