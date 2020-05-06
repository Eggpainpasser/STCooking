import baostock as bs
import pandas as pd
import datetime
from configparser import RawConfigParser

from .defines import kStockConfigPath, kStockCodeKey, kStockRecordCircleKey, \
    kStockRecordFieldsKey, kStockRecordFrequencyKey, kStockRecordAdjustflagKey, \
    kDataEngineBaoStock
from .check import CheckKeyOrDefault, CheckExistKey, CheckKeyOrAbort
from .defines import kStockConfigPath
from .logger_instance import LoggerInstance

class BaoReader(object):
    def __init__(self):
        self._LoadDate()
        self._LoadConfigs()
        self._engine_name = kDataEngineBaoStock
        result = bs.login()
        LoggerInstance.getLogger("stock_info").info('login respond error_code:' + result.error_code)
        LoggerInstance.getLogger("stock_info").info('login respond error_msg :' + result.error_msg)

    def _LoadDate(self):
        self.datetime_ = datetime.datetime.now()

    def _LoadConfigs(self):
        config_parser = RawConfigParser()
        config_parser.read(kStockConfigPath)
        self.data_fields_    = config_parser.get('info', 'default_fields')
        self.data_circle_    = int(config_parser.get('info', 'default_data_circle'))
        self.data_frequency  = config_parser.get('info', 'default_data_frequency')
        self.data_adjustflag = config_parser.get('info', 'default_data_adjustflag')
        self.date_format_ = config_parser.get('info', 'default_date_format')

    def EngineName(self):
        return kDataEngineBaoStock
    
    def GetStockList(self, *args, **kwargs):
        stocklist_handler = bs.query_stock_industry()
        stocklist         = stocklist_handler.get_data()
        return stocklist

    def GetHistoryStockPriceRecord(self, *args, **kwargs):
        post_data_code       = CheckKeyOrAbort(kStockCodeKey, kwargs)
        post_data_fields     = CheckKeyOrDefault(kStockRecordFieldsKey, kwargs, self.data_fields_)
        post_data_circle     = CheckKeyOrDefault(kStockRecordCircleKey, kwargs, self.data_circle_)
        post_data_frequency  = CheckKeyOrDefault(kStockRecordFrequencyKey, kwargs, self.data_frequency)
        post_data_adjustflag = CheckKeyOrDefault(kStockRecordAdjustflagKey, kwargs, self.data_adjustflag)

        post_current_date     = self.datetime_.strftime(self.date_format_)
        post_start_date       = (self.datetime_ - datetime.timedelta(days=post_data_circle)).strftime(self.date_format_)

        stock_history_handler = bs.query_history_k_data_plus(post_data_code, post_data_fields, start_date = post_start_date,
            end_date = post_current_date, frequency = post_data_frequency, adjustflag = post_data_adjustflag)
        stock_history         = stock_history_handler.get_data()
        return stock_history

    def GetCurrentStockFundamentals(self, *args, **kwargs):
        post_data_code   = CheckKeyOrAbort(kStockCodeKey, kwargs)

        profit_data_handler      = bs.query_profit_data(post_data_code)
        profit_data              = profit_data_handler.get_data()
        operation_data_handler   = bs.query_operation_data(post_data_code)
        operation_data           = operation_data_handler.get_data()
        growth_data_handler      = bs.query_growth_data(post_data_code)
        growth_data              = growth_data_handler.get_data()
        balance_data_handler     = bs.query_balance_data(post_data_code)
        balance_data             = balance_data_handler.get_data()
        cash_flow_data_handler   = bs.query_balance_data(post_data_code)
        cash_flow_data           = cash_flow_data_handler.get_data()
        dupont_data_handler      = bs.query_dupont_data(post_data_code)
        dupont_data              = dupont_data_handler.get_data()
        performance_data_handler = bs.query_performance_express_report(post_data_code)
        performance_data         = performance_data_handler.get_data()
        forecast_data_handler    = bs.query_forecast_report(post_data_code)
        forecast_data            = forecast_data_handler.get_data()

        return profit_data, operation_data, growth_data, balance_data, cash_flow_data, dupont_data, performance_data, forecast_data
        

    