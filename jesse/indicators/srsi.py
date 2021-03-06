from collections import namedtuple

import numpy as np
import talib
import tulipy as ti

from jesse.helpers import get_candle_source

StochasticRSI = namedtuple('StochasticRSI', ['k', 'd'])


def srsi(candles: np.ndarray, period=14, period_stoch=14, k=3, d=3, source_type="close", sequential=False) -> StochasticRSI:
    """
    Stochastic RSI

    :param candles: np.ndarray
    :param period: int - default: 14 - RSI Length
    :param period_stoch: int - default: 14 - Stochastic Length
    :param k: int - default: 3
    :param d: int - default: 3
    :param source_type: str - default: "close"
    :param sequential: bool - default=False

    :return: StochasticRSI(k, d)
    """
    if not sequential and len(candles) > 240:
        candles = candles[-240:]

    source = get_candle_source(candles, source_type=source_type)
    rsi_np = talib.RSI(source, timeperiod=period)
    rsi_np = rsi_np[np.logical_not(np.isnan(rsi_np))]
    fast_k, fast_d = ti.stoch(rsi_np, rsi_np, rsi_np, period_stoch, k, d)

    if sequential:
        fast_k = np.concatenate((np.full((candles.shape[0] - fast_k.shape[0]), np.nan), fast_k), axis=0)
        fast_d = np.concatenate((np.full((candles.shape[0] - fast_d.shape[0]), np.nan), fast_d), axis=0)
        return StochasticRSI(fast_k, fast_d)
    else:
        return StochasticRSI(fast_k[-1], fast_d[-1])
