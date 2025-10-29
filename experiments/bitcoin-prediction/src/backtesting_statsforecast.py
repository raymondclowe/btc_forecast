"""Compatibility shim: original code imported `backtesting_statsforecast`.
This file forwards to `backtesting.py` which contains `BitcoinBacktester`.
"""
from backtesting import BitcoinBacktester

__all__ = ["BitcoinBacktester"]
