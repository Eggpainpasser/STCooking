import numpy as np
import pandas as pd

from tum_base.baoreader    import BaoReader
from tum_base.defines      import kValueKeyDate, kValueKeyOpen, kValueKeyHigh, \
                                kValueKeyLow, kValueKeyClose, kValueKeyVolume, \
                                kValueKeyPreclose,  \
                                kSimulatorOperationBuy, kSimulatorOperationSell, \
                                kSimulatorPriceKey, kSimulatorPositionLocKey, \
                                kSimulatorOperationKey, \
                                kDataEngineRaw, kSimulatorDataTodayPrefix, \
                                kSimulatorDataToday, kSimulatorSupportDataKeys
from tum_base.check        import CheckGE, CheckLE, CheckKeyOrAbort
from .                     import __name__ as ModuleName
from .simulator            import Simulator
from charts.quota          import support_quotas, quota_call_from_str
from charts.bandi_recorder import BandiRecorder
from charts.frame          import Frame

class Single_Stock_Simulator(Simulator):
    def __init__(self, st_code, start_date, end_date, data_reader, strategy, fund_manager, trade_manager):
        super(Single_Stock_Simulator, self).__init__()
        self.data_reader   = data_reader
        self.data_engine   = self.data_reader.EngineName()
        self.strategy      = strategy
        self.fund_manager  = fund_manager
        self.trade_manager = trade_manager
        self.bandi_recorder= BandiRecorder()
        self.st_code       = st_code
        self.start_date    = start_date
        self.end_date      = end_date
        
        self.current_index = -1
        self._LoadData()
        self._LoadStrategy()
        self._SelectData()
        self._InitPictureHandler()


    def _LoadData(self):
        self.data = self.data_reader.GetHistoryStockPriceRecord(
            st_code=self.st_code, record_cycle=365)
        self.nrow = self.data.shape[0]
        if self.data_engine is not kDataEngineRaw:
            self._TransformDataFormat()

    def _LoadStrategy(self):
        self.strategy_required_quota  = self.strategy.RequiredQuota()
        self.strategy_required_circle = self.strategy.RequiredDataCircle()
        for quota in self.strategy_required_quota:
            for support_quota in support_quotas:
                if not quota.startswith(support_quota):
                    continue
                quota_data = quota_call_from_str(self.data[kValueKeyOpen[kDataEngineRaw]].astype('float'), 
                                                    self.data[kValueKeyHigh[kDataEngineRaw]].astype('float'),
                                                    self.data[kValueKeyLow[kDataEngineRaw]].astype('float'),
                                                    self.data[kValueKeyClose[kDataEngineRaw]].astype('float'),
                                                    self.data[kValueKeyVolume[kDataEngineRaw]].astype('float'),
                                                    quota)
                self.data[quota] = quota_data


    def _SelectData(self):
        self.data = self.data[self.data[kValueKeyDate[kDataEngineRaw]] <= self.end_date]
        self.data = self.data[self.data[kValueKeyDate[kDataEngineRaw]] >= self.start_date]
        self.nrow = self.data.shape[0]

    def _InitPictureHandler(self):
        self.picture_handler = Frame(self.data, kDataEngineRaw, True)

    def _TransformDataFormat(self):
        pass

    
    def _DataInNeed(self, index):
        CheckGE(index, self.strategy_required_circle, ModuleName)
        data_dict = {}
        for quota in self.strategy_required_quota:
            if quota.startswith(kSimulatorDataTodayPrefix):
                CheckKeyOrAbort(quota, kSimulatorSupportDataKeys)
                if quota == kSimulatorDataToday.format(data_key=kValueKeyOpen[kDataEngineRaw]):
                    data_dict[quota] = self.data[quota][index + 1]
            else:
                data_dict[quota] = self.data[quota][index - self.strategy_required_circle : index]
        return data_dict

    def NextDay(self):
        self.current_index += 1
        print(self.current_index, self.nrow)
        if(self.current_index >= self.nrow):
            return False
        date = self.data[kValueKeyDate[kDataEngineRaw]].iloc[self.current_index]
        pd_date = pd.to_datetime(date)
        self.bandi_recorder.NewRecord(pd_date, self.fund_manager.TotalFund() / self.fund_manager.InitFund())
        self.bandi_recorder.NewReference(pd_date, 
            float(self.data[kValueKeyClose[kDataEngineRaw]].iloc[self.current_index]) / float(self.data[kValueKeyClose[kDataEngineRaw]].iloc[0]))

        if self.current_index < self.strategy_required_circle:
            return True
        date = self.data[kValueKeyDate[kDataEngineRaw]].iloc[self.current_index]
        data_dic = self._DataInNeed(self.current_index)
        
        # self.st_code make a decision
        operation    = self.strategy.MakeDecision(data_dic)
        operate_name = operation[kSimulatorOperationKey]
        position_loc = float(operation[kSimulatorPositionLocKey])
        price        = float(operation[kSimulatorPriceKey])
        if operate_name == kSimulatorOperationBuy:
            self._BuyProcess(self.st_code, price, position_loc)
        if operate_name == kSimulatorOperationSell:
            self._SellProcess(self.st_code, price, position_loc)

        
        # after a day, update the stock price 
        st_price_dict = {self.st_code : float(self.data[kValueKeyClose[kDataEngineRaw]].iloc[self.current_index])}
        self.fund_manager.UpdateStocksInfo(st_price_dict)

        self.trade_manager.CloseOfTheDay() 
        return True       
        
        
    def DrawSummary(self):
        self.fund_manager.LogSummary()
        self.picture_handler.Capture(0, extra_series=self.bandi_recorder.FrameFormat())
 

    def _BuyProcess(self, st_code, price, position_loc):
        enable_cost_money = self.fund_manager.FreeFundPositionMoney(position_loc)
        enable_buy_nums, real_buy_price = self.trade_manager.PrepareToBuy(
                                self.st_code, enable_cost_money, price, 
                                float(self.data[kValueKeyPreclose[kDataEngineRaw]].iloc[self.current_index]),
                                float(self.data[kValueKeyOpen[kDataEngineRaw]].iloc[self.current_index]),
                                float(self.data[kValueKeyHigh[kDataEngineRaw]].iloc[self.current_index]),
                                float(self.data[kValueKeyLow[kDataEngineRaw]].iloc[self.current_index]))
        real_cost_money   = self.trade_manager.RealBuyCostMoney(real_buy_price, enable_buy_nums)
        if enable_buy_nums > 0:
            self.fund_manager.Buy(self.st_code, enable_buy_nums, real_cost_money)

    def _SellProcess(self, st_code, price, position_loc):
        plan_sell_nums  = self.fund_manager.StockHoldPositionNum(self.st_code, position_loc)
        enable_sell_nums, real_sell_price = self.trade_manager.PrepareToSell(
                                    self.st_code, plan_sell_nums, price, 
                                    float(self.data[kValueKeyPreclose[kDataEngineRaw]].iloc[self.current_index]),
                                    float(self.data[kValueKeyOpen[kDataEngineRaw]].iloc[self.current_index]),
                                    float(self.data[kValueKeyHigh[kDataEngineRaw]].iloc[self.current_index]),
                                    float(self.data[kValueKeyLow[kDataEngineRaw]].iloc[self.current_index]))
        if enable_sell_nums > 0:
            real_earn_money = self.trade_manager.RealSellEarnMoney(real_sell_price, enable_sell_nums)
            self.fund_manager.Sell(self.st_code, real_earn_money)





        

        