from tum_base.check import CheckLE, CheckKeyOrAbort
from . import __name__ as ModuleName

kCodeKey   = 'code'
kNumberChg = 'num_chg'
kHoldNumber= 'num'
kHoldDays  = 'hold_days'

class TradeRecorder(object):
    def __init__(self, trade_period = 1):
        self.trade_period = trade_period
        self.bought_info  = {kCodeKey:[], kNumberChg:[], kHoldDays:[]}
        self.hold_st_info = {}

    def NewTrade(self, st_code, trade_num):
        if trade_num == 0:
            return
        if trade_num > 0:
            self.bought_info[kCodeKey].append(st_code)
            self.bought_info[kNumberChg].append(trade_num)
            self.bought_info[kHoldDays].append(0)
            self._RefreshHoldInfo()
        if trade_num < 0:
            CheckKeyOrAbort(st_code, self.hold_st_info)
            CheckLE(trade_num, self.hold_st_info, ModuleName)
            self.hold_st_info[st_code] -= trade_num
            if self.hold_st_info[st_code] == 0:
                del self.hold_st_info[st_code]


    def NextDay(self):
        for i in range(len(self.bought_info[kCodeKey])):
            self.bought_info[kHoldDays][i] += 1
        self._RefreshHoldInfo()
        

    def EnableSellNum(self, st_code):
        if st_code not in self.hold_st_info:
            return 0
        else:
            return self.hold_st_info[st_code]

    def _RefreshHoldInfo(self):
        for i in reversed(range(len(self.bought_info[kCodeKey]))):
            if self.bought_info[kHoldDays][i] >= self.trade_period:
                st_code    = self.bought_info[kCodeKey][i]
                number_chg = self.bought_info[kNumberChg][i]
                if st_code not in self.hold_st_info:
                    self.hold_st_info[st_code] = number_chg
                else:
                    self.hold_st_info[st_code] += number_chg
                self.bought_info[kCodeKey].pop(i)
                self.bought_info[kNumberChg].pop(i)
                self.bought_info[kHoldDays].pop(i)
