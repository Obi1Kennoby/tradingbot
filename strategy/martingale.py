from strategy.base import BaseStrategy


class Order:
    def __init__(self, total, price):
        self.total = total
        self.price = price
        self.quantity = total / price

    def get_percent(self, current_price):
        current_total = current_price * self.quantity
        increase = current_total - self.total
        return increase / self.total * 100


class Martingale(BaseStrategy):
    def __init__(self, historical, commission, order_percent=1):
        super().__init__(historical, commission)
        self.order_percent = order_percent
        self.is_long = False
        self.is_short = False
        self.long_times = 0
        self.short_times = 0
        self.base_order_amount = 100  # self.money / 10
        self.current_order_amount = self.base_order_amount
        self.order = None
        self.terminated = False

    def long(self, price, money_amount):
        self.close_all(price)
        if money_amount > self.money:
            self.terminate()
            return
        self.is_long = True
        self.bought_quantity = money_amount / price
        self.order = Order(money_amount, price)
        self.pay_commission(money_amount)
        self.long_times += 1

    def short(self, price, money_amount):
        self.close_all(price)
        if money_amount > self.money:
            self.terminate()
            return
        self.is_short = True
        self.bought_quantity = money_amount / price
        self.order = Order(money_amount, price)
        self.pay_commission(money_amount)
        self.short_times += 1

    def close_all(self, price):
        if self.bought_quantity != 0:
            current_sum = self.bought_quantity * price
            if self.is_long:
                self.money += current_sum - self.order.total
            else:
                self.money += self.order.total - current_sum

            self.pay_commission(current_sum)
            self.bought_quantity = 0

            self.is_long = False
            self.is_short = False
            self.order = None

    def terminate(self):
        print('Oops you are out of money')
        self.terminated = True

    def run(self):
        last_price = 0
        for index, row in self.historical.iterrows():

            if self.terminated:
                break

            last_price = float(row['c'])

            # very first order
            if self.order is None:
                self.long(last_price, self.base_order_amount)
                continue

            percent_diff = self.order.get_percent(last_price)
            if self.is_long is True:
                # successful order, start from the base amount
                if percent_diff >= self.order_percent:
                    self.current_order_amount = self.base_order_amount
                    self.long(last_price, self.base_order_amount)
                # failed order, increase order amount
                elif percent_diff <= -self.order_percent:
                    self.current_order_amount *= 2
                    self.short(last_price, self.current_order_amount)
                continue
            else:
                # successful order, start from the base amount
                if percent_diff <= -self.order_percent:
                    self.current_order_amount = self.base_order_amount
                    self.short(last_price, self.base_order_amount)
                # failed order, increase order amount
                elif percent_diff >= self.order_percent:
                    self.current_order_amount *= 2
                    self.long(last_price, self.current_order_amount)
                continue

        self.close_all(last_price)

    def show_money(self):
        print("MONEY: " + str(self.money))
        print("Long times: " + str(self.long_times))
        print("Short times: " + str(self.short_times))
        print("commission: " + str(self.commission_paid))
        print("net: " + str(self.get_money_net()))