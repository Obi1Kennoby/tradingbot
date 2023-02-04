from abc import ABC, abstractmethod

START_MONEY = 10000
COMMISSION = 0.1


class BaseStrategy(ABC):
    def __init__(self, historical, commission: float = COMMISSION):
        self.historical = historical
        self.money = START_MONEY
        self.commission = commission
        self.commission_paid = 0
        self.bought_quantity = 0
        super().__init__()

    def pay_commission(self, amount: float):
        self.commission_paid += amount / 100 * self.commission

    def get_money(self):
        return self.money

    def get_money_net(self):
        return self.money - self.commission_paid

    def get_commission(self):
        return self.commission

    @abstractmethod
    def run(self):
        pass
