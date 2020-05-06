from traceback import format_stack
from json import dumps

from .logger_instance import LoggerInstance

def TracebackPhase():
    trace_back_lists = format_stack()
    trace_back_phase = ''
    for trace_back_info in trace_back_lists[:-2]:
        trace_back_phase += trace_back_info
    return trace_back_phase

def CheckExistKey(key, dic):
    return key in dic

def CheckKeyOrDefault(key, dic, default_value):
    if CheckExistKey(key, dic):
        return dic[key]
    return default_value

def CheckKeyOrAbort(key, dic, logger_name = 'base'):
    if CheckExistKey(key, dic):
        return dic[key]
    #error_phase = 'Check Key Error. Key : |%s| not in the dic |%s|' %(key, dumps(dic))
    error_phase = 'Check Key Error. Key : |%s| not in the dic' %(key)
    trace_back_phase = TracebackPhase()
    output_msg = '%s \n trace_back :\n %s' %(error_phase, trace_back_phase)
    LoggerInstance.getLogger(logger_name).error(output_msg)
    raise Exception(output_msg)

def CheckGE(value, reference_value, logger_name = 'base'):
    if value >= reference_value:
        return True
    error_phase = 'Check Value. Assert |{value}| >= |{reference_value}|'.format(value=value, reference_value=reference_value)
    trace_back_phase = TracebackPhase()
    output_msg = '{error_phase} from:\n {stack_phase}'.format(error_phase=error_phase, stack_phase=trace_back_phase)
    LoggerInstance.getLogger(logger_name).error(output_msg)
    raise Exception(output_msg)

def CheckLE(value, reference_value, logger_name = 'base'):
    if value <= reference_value:
        return True
    error_phase = 'Check Value. Assert |{value}| <= |{reference_value}|'.format(value=value, reference_value=reference_value)
    trace_back_phase = TracebackPhase()
    output_msg = '{error_phase} from:\n {stack_phase}'.format(error_phase=error_phase, stack_phase=trace_back_phase)
    LoggerInstance.getLogger(logger_name).error(output_msg)
    raise Exception(output_msg)


