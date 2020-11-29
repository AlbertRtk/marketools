import pandas as pd


class Commission:
    def __init__(self, rate: float, minimum: float):
        if minimum < 0:
            raise ValueError('minimum has to be non-negative value')
        if rate <= 0:
            raise ValueError('rate has to be positive value')

        self.rate = rate
        self.minimum = minimum

    def __call__(self, trade: float, *args, **kwargs) -> float:
        fee = trade * self.rate
        fee = round(fee, 2)
        return max(fee, self.minimum)

    def minimal_recommended_investment(self):
        return self.minimum / self.rate


class Wallet(Commission):
    def __init__(self, commission_rate: float, min_commission):
        super().__init__(commission_rate, min_commission)
        self.money = 0
        self.stocks = pd.DataFrame(columns=['Name', 'Volume', 'Purchase price', 'Price'])

    @property
    def money(self) -> float:
        return self.__money

    @property
    def stocks(self) -> pd.DataFrame:
        return self.__stocks

    @property
    def stocks_value(self):
        values = self.stocks.loc[:, ('Volume', 'Price')].product(axis=1)
        return values.sum()

    @property
    def total_value(self):
        return self.stocks_value + self.money

    @money.setter
    def money(self, pay_in: float):
        self.__money = pay_in

    @stocks.setter
    def stocks(self, new_stocks: pd.DataFrame):
        self.__stocks = new_stocks

    def __str__(self) -> str:
        return f'Stocks: \n' \
               f'{self.stocks} \n\n' \
               f'Stocks value: \t {self.stocks_value} \n' \
               f'Money: \t\t\t {self.money} \n' \
               f'Total value: \t {self.total_value} \n'

    def __add__(self, other: pd.DataFrame):
        """

        :param other: pd.DataFrame with columns 'Name', 'Volume', 'Purchase price', 'Price'
        :return:
        """
        """ added values """
        name = other.loc[0, 'Name']
        bought = other.loc[0, 'Volume']
        price = other.loc[0, 'Purchase price']

        """ owned stocks with same name """
        in_wallet = self.get_volume_of_stocks(name)
        wallet_price = self.get_purchase_price_of_stocks(name)

        """ calculate cost """
        cost = bought * price
        cost += self(cost)

        """ enough money in wallet to buy? """
        if cost <= self.money:
            if not in_wallet:
                """ stocks not in wallet - append them """
                self.stocks = self.stocks.append(other, ignore_index=True)
            else:
                """ stocks in wallet - increase volume and calculate average purchase price """
                idx = self.__get_stocks_index(name)
                self.stocks.loc[idx, 'Volume'] += bought
                self.stocks.loc[idx, 'Price'] = price
                avg_price = (price * bought + wallet_price * in_wallet) / (bought + in_wallet)
                self.stocks.loc[idx, 'Purchase price'] = avg_price

            self.money -= cost

        return self

    def __sub__(self, other: pd.DataFrame):
        """

        :param other: pd.DataFrame with columns 'Name', 'Volume', 'Price'
        :return:
        """
        """ subtracted values """
        name = other.loc[0, 'Name']
        sold = other.loc[0, 'Volume']
        price = other.loc[0, 'Price']

        """ owned stocks with the same name """
        in_wallet = self.get_volume_of_stocks(name)

        if in_wallet >= sold > 0:
            idx = self.__get_stocks_index(name)
            if in_wallet == sold:
                """ all stocks from wallet solc - drop them """
                self.stocks = self.stocks.drop(idx)
            else:
                """ part of stocks from wallet sold - decrease volume """
                self.stocks.loc[idx, 'Volume'] -= sold
                self.stocks.loc[idx, 'Price'] = price

            """ calculate gain """
            gain = sold * price
            gain -= self(gain)
            self.money += gain

        return self

    def __get_stocks_index(self, name: str):
        idx = self.stocks.index[self.stocks['Name'] == name].tolist()
        idx = idx[0] if idx else None
        return idx

    def get_volume_of_stocks(self, name: str) -> int:
        idx = self.__get_stocks_index(name)
        if idx is not None:
            return self.stocks.loc[idx, 'Volume']
        else:
            return 0

    def get_purchase_price_of_stocks(self, name: str):
        idx = self.__get_stocks_index(name)
        if idx is not None:
            return self.stocks.loc[idx, 'Purchase price']
        else:
            return None

    def buy(self, name: str, volume: int, price: float) -> None:
        stock = pd.DataFrame({'Name': [name],
                              'Volume': [volume],
                              'Purchase price': [price],
                              'Price': [price]})
        self.__add__(stock)

    def sell(self, name: str, volume: int, price: float) -> None:
        stock = pd.DataFrame({'Name': [name],
                              'Volume': [volume],
                              'Price': [price]})
        self.__sub__(stock)

    def sell_all(self, name: str, price: float) -> None:
        volume = self.get_volume_of_stocks(name)
        self.sell(name, volume, price)
        return volume

    def list_stocks(self) -> list:
        return self.stocks.loc[:, 'Name'].to_list()

    def update_price(self, name: str, price: float) -> None:
        idx = self.__get_stocks_index(name)
        if idx is not None:
            self.stocks.loc[idx, 'Price'] = price

    def change(self, name: str) -> float:
        idx = self.__get_stocks_index(name)
        purchase_price = self.stocks.loc[idx, 'Purchase price']
        price = self.stocks.loc[idx, 'Price']
        output = (price - purchase_price) / purchase_price
        return output


def calculate_investment_value(wallet, max_positions):
    output = 0
    min_value = wallet.minimal_recommended_investment()
    if wallet.money > min_value:
        max_value = wallet.total_value / max_positions
        output = max(max_value, min_value)
        output = min(output, wallet.money)
    return output
    