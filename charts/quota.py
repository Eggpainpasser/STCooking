import numpy as np

from tum_base.logger_instance import LoggerInstance
from . import __name__ as ModuleName


support_quotas = ['ma_', 'rsi_', 'k_', 'd_', 'j_']

def quota_call_from_str(opens, highs, lows, closes, volumes, quota_str):
    if(quota_str.startswith('ma_')):
        circle = int(quota_str[3:])
        return moving_average(closes, circle)
    if(quota_str.startswith('rsi_')):
        circle = int(quota_str[4:])
        return relative_strength(closes, circle)
    if(quota_str.startswith('k_')):
        circle = int(quota_str[2:])
        return stochastics(highs, lows, closes, circle)['K']
    if(quota_str.startswith('d_')):
        circle = int(quota_str[2:])
        return stochastics(highs, lows, closes, circle)['D']
    if(quota_str.startswith('j_')):
        circle = int(quota_str[2:])
        return stochastics(highs, lows, closes, circle)['J']
    LoggerInstance.getLogger(ModuleName).error('Unsupport quota name: %{quota_name}'.format(quota_name=quota_str))

def moving_average(prices, n):
    prices = np.asarray(prices)
    weights = np.ones(n)
    weights /= weights.sum()
    
    result = np.convolve(prices, weights, mode='full')[:len(prices)]
    result[:n] = result[n]
    return result

def relative_strength(prices, n=14):
    deltas  = np.diff(prices)
    seed    = deltas[:n + 1]
    up      = seed[seed >= 0].sum() / n
    down    = -seed[seed < 0].sum() / n
    rsi     = np.zeros_like(prices)
    rsi[:n] = 50

    for i in range(n, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up   = (up * (n - 1) + upval) / n
        down = (down * (n - 1) + downval) / n

        rs   = up / down
        rsi[i] = 100. - 100. / (1. + rs)
    return rsi

def stochastics(highs, lows, closes, n):
    assert len(highs) == len(lows) == len(closes)
    K = np.zeros_like(highs)
    D = np.zeros_like(highs)
    J = np.zeros_like(highs)

    K[:n] = 50
    D[:n] = 50
    J[:n] = 50
    Kn    = 50.
    Dn    = 50.
    for i in range(n, len(highs)):
        Cn   = closes[i]
        Hn   = max(highs[i - n:i + 1])
        Ln   = min(lows[i - n:i + 1])
        rsv  = (Cn - Ln) / (Hn - Ln) * 100.

        K[i] = Kn * 2. / 3. + rsv  * 1. / 3.
        D[i] = Dn * 2. / 3. + K[i] * 1. / 3.
        J[i] = 3. * K[i] - 2. * D[i]
    data_dic = {'K' : K, 'D' : D, 'J' : J}
    return data_dic 



    

