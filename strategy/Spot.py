from strategy.base import BaseStrategy

START_MONEY = 10000
BID = 500
BUY_TRIGGER = 90
SELL_TRIGGER = -70  # -30, -40, -50, -70
COMMISSION = 0.1


class Spot(BaseStrategy):
    def __init__(self, historical, buy_trigger=BUY_TRIGGER, sell_trigger=SELL_TRIGGER, commission=COMMISSION):
        super().__init__(historical, commission)
        self.buyTimes = 0
        self.sellTimes = 0
        self.buy_trigger = buy_trigger
        self.sell_trigger = sell_trigger

    def buy(self, price):
        self.money -= BID
        self.bought_quantity += BID / price
        self.pay_commission(BID)
        self.buyTimes += 1

    def sell(self, price):
        if self.bought_quantity != 0:
            sum_sell = self.bought_quantity * price
            self.money += sum_sell
            self.pay_commission(sum_sell)
            self.bought_quantity = 0
            self.sellTimes += 1

    def run(self):
        last_price = 0
        for index, row in self.historical.iterrows():
            sum = float(row['SUM'])
            last_price = float(row['c'])
            if sum > 0:  # row['STATUS'] == 'Bull':
                if sum > self.buy_trigger:
                    self.buy(last_price)
            elif sum < 0:  # row['STATUS'] == 'Bear':
                if sum < self.sell_trigger:
                    self.sell(last_price)

        self.sell(last_price)
        # self.show_money()

    def show_money(self):
        print("MONEY: " + str(self.money))
        print("Buy times: " + str(self.buyTimes))
        print("Sell times: " + str(self.sellTimes))
        print("commission: " + str(self.commission_paid))
        print("net: " + str(self.get_money_net()))

    def get_bid(self):
        return BID


class Features(BaseStrategy):
    def __init__(self, historical, buy_trigger=BUY_TRIGGER, sell_trigger=SELL_TRIGGER, close_long=-10, close_short=10, commission=COMMISSION):
        super().__init__(historical, commission)
        self.buy_trigger = buy_trigger
        self.sell_trigger = sell_trigger
        self.close_long = close_long
        self.close_short = close_short
        self.is_long = False
        self.is_short = False
        self.long_times = 0
        self.short_times = 0

    def long(self, price):
        self.close_all(price)
        self.is_long = True
        self.bought_quantity = self.money / price
        self.pay_commission(self.money)
        self.long_times += 1

    def short(self, price):
        self.close_all(price)
        self.is_short = True
        self.bought_quantity = self.money / price
        self.pay_commission(self.money)
        self.short_times += 1

    def close_all(self, price):
        if self.bought_quantity != 0:
            current_sum = self.bought_quantity * price
            if self.is_long:
                self.money += current_sum - self.money
            else:
                self.money += self.money - current_sum

            self.pay_commission(current_sum)
            self.bought_quantity = 0

            self.is_long = False
            self.is_short = False

    def run(self):
        last_price = 0
        for index, row in self.historical.iterrows():
            sum = float(row['SUM'])

            # if sum > 0:
            #     sum = -sum
            # elif sum < 0:
            #     sum = abs(sum)

            last_price = float(row['c'])

            if (self.is_long is True and sum < self.close_long) or (self.is_short is True and sum > self.close_short):
                self.close_all(last_price)

            if sum > self.buy_trigger:
                if self.is_long is False:
                    self.long(last_price)
            elif sum < self.sell_trigger:
                if self.is_short is False:
                    self.short(last_price)

        self.close_all(last_price)

    def show_money(self):
        print("MONEY: " + str(self.money))
        print("Long times: " + str(self.long_times))
        print("Short times: " + str(self.short_times))
        print("commission: " + str(self.commission_paid))
        print("net: " + str(self.get_money_net()))

