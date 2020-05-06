from tum_base.baoreader               import BaoReader
from charts.frame                     import Frame
from simulator.ab_share_trade_manager import AB_Share_TradeManager
from simulator.fund_manager           import FundManager
from simulator.single_stock_simulator import Single_Stock_Simulator
from simulator.strategy               import Strategy

if __name__ == '__main__':
    data_reader = BaoReader()
    strategy = Strategy()
    fd  = FundManager(10000.)
    trade_manager = AB_Share_TradeManager(0.025, 0.025)
    sim = Single_Stock_Simulator('sz.000066','2019-10-01', '2020-04-06', data_reader, strategy, fd, trade_manager)
    while(sim.NextDay()):
        pass
    sim.DrawSummary()
    #data_reader = BaoReader()
    #frame = Frame('sz.000066', 730, data_reader)
    #frame.Capture(0)

    #trade_manager = ABTradeManager(5,5)
    #frame = Frame('sz.000066')
    #frame.Capture(0)
