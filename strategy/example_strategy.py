from .strategy import Strategy
class ExampleStrategy(Strategy):
    def __init__(self):
        pass
    def RequiredQuota(self):
        pass
        return ['low','rsi_14', 'k_12', 'd_12', 'j_12', 'ma_5', 'ma_10']
    def RequiredDataCircle(self):
        pass
        return 5
    def MakeDecision(self, data_dic):
        pass
        #print(data_dic)
        chg_position_loc = 0.5
        buy_price        = 100
        return {kSimulatorOperationKey:kSimulatorOperationBuy, kSimulatorPriceKey:100, kSimulatorPositionLocKey:0.8}