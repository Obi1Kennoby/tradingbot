from strategy.Spot import Spot, Features
from strategy.martingale import Martingale
from tools.collect_data import get_all_candles_with_patterns, get_candles_with_patterns

BUY_RANGE = 400
SELL_RANGE = -200
STEP = 100


def show_spot_strategies():
    historicals = get_candles_with_patterns('BTCUSDT', '4w', '5m')  # get_all_candles_with_patterns()

    best = 0
    best_buy_trigger = 0
    best_buy_times = 0
    best_sell_trigger = 0
    best_sell_times = 0

    # st = Spot(historicals, buy_trigger=80, sell_trigger=-80, commission=0.1)
    # st.run()
    # st.show_money()

    # st = Features(historicals, buy_trigger=150, sell_trigger=-75, close_long=-20, close_short=40, commission=0.1)
    # st.run()
    # st.show_money()

    st = Martingale(historicals, commission=0.04)
    st.run()
    st.show_money()


    # for historical in [historicals]:
    #     for i in range(0, BUY_RANGE, STEP):
    #         for j in range(SELL_RANGE, 0, STEP):
    #             st = Spot(historical, buy_trigger=i, sell_trigger=j)
    #             st.run()
    #             money = st.get_money_net()
    #             if money > best and st.buyTimes > 10:
    #                 best = money
    #                 best_buy_trigger = i
    #                 best_buy_times = st.buyTimes
    #
    #                 best_sell_trigger = j
    #                 best_sell_times = st.sellTimes
    #
    #     __print_statistic('BTCUSDT', '1w', '1h', best, best_buy_trigger, best_sell_trigger)


def __print_statistic(symbol, range, interval, money, buy_trigger, sell_trigger):
    text = f"""
symbol: {symbol}
range: {range}
interval: {interval}
money: {money}
buy_trigger: {buy_trigger} 
sell_trigger: {sell_trigger}
"""

    print(text)
