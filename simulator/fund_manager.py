from tum_base.check import CheckGE, CheckLE, CheckKeyOrAbort
from . import __name__ as ModuleName


class FundManager(object):
    def __init__(self, init_fund):
        self.init_fund    = init_fund
        self.free_fund    = init_fund
        self.control_fund = 0.
        self.st_summary   = {}
        self.st_holds     = {}
        self.st_prices    = {}

    def Buy(self, st_code, trade_num, cost_money):
        CheckGE(self.free_fund, cost_money, ModuleName)

        if st_code not in self.st_holds:
            self.st_prices[st_code] = cost_money / trade_num
            self.st_holds[st_code]  = trade_num
        else:
            self.st_prices[st_code] = \
                (self.st_holds[st_code] * self.st_prices[st_code] + cost_money) \
                / (self.st_holds[st_code] + trade_num)
            self.st_holds[st_code]  += trade_num
        
        self.free_fund -= cost_money
        self._Refresh()
        self._AddSummary(st_code, -cost_money)

    def Sell(self, st_code, trade_num, earn_money):
        CheckKeyOrAbort(st_code, self.st_holds, ModuleName)
        CheckGE(self.st_holds[st_code], trade_num, ModuleName)

        if(self.st_holds[st_code] == trade_num):
            del self.st_holds[st_code]
            del self.st_prices[st_code]
        else:
            self.st_prices[st_code] = \
                (self.st_holds[st_code] * self.st_prices[st_code] - earn_money) \
                / (self.st_holds[st_code] - trade_num)
            self.st_holds[st_code] -= trade_num
        self.free_fund += earn_money
        self._Refresh()
        self._AddSummary(st_code, earn_money)

    def HoldStock(self, st_code):
        if st_code not in self.st_holds:
            return 0
        return self.st_holds[st_code]

    def UpdateStocksInfo(self, st_price_dict):
        self.st_prices  = st_price_dict
        self._Refresh()

    def FreeFund(self):
        return self.free_fund

    def ControlFund(self):
        return self.control_fund

    def TotalFund(self):
        return self.control_fund + self.free_fund

    def InitFund(self):
        return self.init_fund

    def Position(self):
        return self.control_fund / (self.control_fund + self.free_fund)
    
    def FreeFundPositionMoney(self, position):
        CheckLE(position, 1., ModuleName)
        return self.free_fund * position
    
    def StockHoldPositionNum(self, st_code, position):
        CheckLE(position, 1., ModuleName)
        if(st_code not in self.st_holds):
            return 0
        return self.st_holds[st_code] * position

    def STHoldSummary(self):
        hold_summary = {}
        for st_code in self.st_summary:
            earn_money = self.st_summary[st_code]
            if st_code in self.st_holds:
                earn_money += self.st_holds[st_code] * self.st_prices[st_code]
            hold_summary[st_code] = earn_money
        return hold_summary

    def LogSummary(self):
        total_earn = 0.
        hold_summary = self.STHoldSummary()
        for st_code in hold_summary:
            total_earn += float(hold_summary[st_code])
        log_format = '{st_code:10s} earned {earn_money}({percentage:3.2f}%)'
        print('========================SUMMARY===========================')
        for st_code in hold_summary:
            print(log_format.format(st_code=st_code, earn_money=hold_summary[st_code], percentage=hold_summary[st_code]/total_earn * 100.))
        print('')
        print('----------------------------------------------------------')
        print(log_format.format(st_code='total', earn_money=total_earn, percentage=total_earn/self.init_fund * 100.))
        print('==================END OF SUMMARY==========================')            
            

    def _Refresh(self):
        self.control_fund = 0.
        for hold_stock in self.st_holds:
            self.control_fund += self.st_holds[hold_stock] * self.st_prices[hold_stock]

    def _AddSummary(self, st_code, money_chg):
        if st_code not in self.st_summary:
            self.st_summary[st_code]  = money_chg
        else:
            self.st_summary[st_code] += money_chg




