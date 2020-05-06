import numpy as np
kStockConfigPath          = 'config/stockinfo.ini'
kStockCodeKey             = 'st_code'
kStockRecordCircleKey     = 'record_cycle'
kStockRecordFieldsKey     = 'record_fields'
kStockRecordFrequencyKey  = 'record_frequency'
kStockRecordAdjustflagKey = 'record_adjustflag'


kDataEngineBaoStock = 'BaoStock'
kDataEngineMPLFinance = 'mplfinance'
kDataEngineRaw = kDataEngineBaoStock
kValueKeyDate       = {kDataEngineBaoStock : 'date',       
                        kDataEngineMPLFinance : 'Date'}
kValueKeyCode       = {kDataEngineBaoStock : 'code',       
                        kDataEngineMPLFinance : 'Code'}
kValueKeyOpen       = {kDataEngineBaoStock : 'open',       
                        kDataEngineMPLFinance : 'Open'}
kValueKeyHigh       = {kDataEngineBaoStock : 'high',       
                        kDataEngineMPLFinance : 'High'}
kValueKeyLow        = {kDataEngineBaoStock : 'low' ,       
                        kDataEngineMPLFinance : 'Low'}
kValueKeyClose      = {kDataEngineBaoStock : 'close',      
                        kDataEngineMPLFinance : 'Close'}
kValueKeyPreclose   = {kDataEngineBaoStock : 'preclose',   
                        kDataEngineMPLFinance : 'PreClose'}
kValueKeyVolume     = {kDataEngineBaoStock : 'volume',     
                        kDataEngineMPLFinance : 'Volume'}
kValueKeyAmount     = {kDataEngineBaoStock : 'amount',     
                        kDataEngineMPLFinance : 'Amount'}
kValueKeyAdjustFlag = {kDataEngineBaoStock : 'adjustflag', 
                        kDataEngineMPLFinance : 'AdjustFlag'}
kValueKeyTurn       = {kDataEngineBaoStock : 'turn',       
                        kDataEngineMPLFinance : 'Turn'}
kValueKeyTradestatus= {kDataEngineBaoStock : 'tradestatus',
                        kDataEngineMPLFinance : 'TradeStatus'}
kValueKeyPctchg     = {kDataEngineBaoStock : 'pctChg',     
                        kDataEngineMPLFinance : 'PctChg'}
kValueKeyPeTTM      = {kDataEngineBaoStock : 'peTTM',      
                        kDataEngineMPLFinance : 'PETTM'}
kValueKeyPbMRQ      = {kDataEngineBaoStock : 'pbMRQ',      
                        kDataEngineMPLFinance : 'PBMRQ'}
kValueKeyPsTTM      = {kDataEngineBaoStock : 'psTTM',      
                        kDataEngineMPLFinance : 'PSTTM'}
kValueKeyPcfNcfTTM  = {kDataEngineBaoStock : 'pcfNcfTTM',  
                        kDataEngineMPLFinance : 'PCFNCFTTM'}
kValueKeyIsST       = {kDataEngineBaoStock : 'isST',       
                        kDataEngineMPLFinance : 'IsST'}


kSimulatorOperationKey    = 'operation'
kSimulatorPriceKey        = 'price'
kSimulatorPositionLocKey  = 'position'
kSimulatorOperationBuy    = 'buy'
kSimulatorOperationSell   = 'sell'

kSimulatorDataTodayPrefix = 'today_'
kSimulatorDataToday       = kSimulatorDataTodayPrefix + '{data_key}'
kSimulatorSupportDataKeys = [kValueKeyOpen[kDataEngineRaw], kValueKeyHigh[kDataEngineRaw],
    kValueKeyLow[kDataEngineRaw], kValueKeyClose[kDataEngineRaw], kValueKeyPreclose[kDataEngineRaw],
    kValueKeyVolume[kDataEngineRaw], kValueKeyAmount[kDataEngineRaw], kValueKeyTurn[kDataEngineRaw],
    kValueKeyPeTTM[kDataEngineRaw], kValueKeyPctchg[kDataEngineRaw], kValueKeyPbMRQ[kDataEngineRaw],
    kValueKeyPsTTM[kDataEngineRaw], kValueKeyPcfNcfTTM[kDataEngineRaw], 
    kSimulatorDataToday.format(data_key=kValueKeyOpen[kDataEngineRaw])]
