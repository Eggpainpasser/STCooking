from .trade_manager import TradeManager
from .trade_recorder import TradeRecorder

class AB_Share_TradeManager(TradeManager):
    def __init__(self, buy_fee_percent, sell_fee_percent, trade_period=1):
        super(AB_Share_TradeManager, self).__init__()
        self.buy_fee_scale          = buy_fee_percent / 100.
        self.sell_fee_scale         = sell_fee_percent / 100.
        self.buy_sell_bias          = 5
        self.extra_fee_scale        = 0.003
        self.buyable_limit_percent  = 1.1
        self.sellable_limit_percent = 0.9
        self.onehandle              = 100
        self.trade_recorder         = TradeRecorder(trade_period)
    
    def PrepareToBuy(self, st_code, free_fund, buy_price, pre_close, open, high, low):
        limit_price = round(self.buyable_limit_percent * pre_close, 2)
        if low == high == limit_price:
            return 0, buy_price
        if buy_price <  low:
            return 0, buy_price
        if buy_price >= limit_price:
            buy_price = open
        # x * buy_price * (1 + fee) = real_cost
        # x = real_cost / (1 + fee) / buy_price
        could_buy_nums = free_fund // ((1. + self.buy_fee_scale) * buy_price)
        if could_buy_nums < self.onehandle:
            return 0, buy_price
        enable_buy_num = could_buy_nums // self.onehandle * self.onehandle

        self.trade_recorder.NewTrade(st_code, enable_buy_num)
        return enable_buy_num, buy_price

    def PrepareToSell(self, st_code, hold_num, sell_price, pre_close, open, high, low):
        limit_price = round(self.sellable_limit_percent * pre_close, 2)
        if sell_price > high:
            return 0, sell_price
        if hold_num == 0:
            return 0, sell_price
        if low == high == limit_price:
            return 0, sell_price
        if sell_price <= limit_price:
            sell_price = open
        enable_sell_num = min(self.trade_recorder.EnableSellNum(st_code), hold_num)
        return enable_sell_num, sell_price

    def RealBuyCostMoney(self, buy_price, buy_nums):
        origin_cost_money   = buy_price * buy_nums
        extra_cost_money    = origin_cost_money * self.extra_fee_scale
        buy_sell_cost_money = max(self.buy_sell_bias, origin_cost_money * self.buy_fee_scale)
        real_cost_money     = origin_cost_money + extra_cost_money + buy_sell_cost_money
        return real_cost_money
    
    def RealSellEarnMoney(self, sell_price, sell_nums):
        origin_earn_money   = sell_price * sell_nums
        extra_cost_money    = origin_earn_money * self.extra_fee_scale
        buy_sell_cost_money = max(self.buy_sell_bias, origin_earn_money * self.buy_fee_scale)
        real_earn_money     = origin_earn_money - extra_cost_money - buy_sell_cost_money
        return real_earn_money

    def CloseOfTheDay(self):
        self.trade_recorder.NextDay()

        
        