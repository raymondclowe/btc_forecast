"""Smoke test to verify basic functionality."""


def test_import_data_utils():
    """Test that data_utils can be imported."""
    import sys
    import os
    
    # Add experiments/bitcoin-prediction to path
    bitcoin_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'experiments', 'bitcoin-prediction'
    )
    sys.path.insert(0, bitcoin_path)
    
    # Test import
    from src import data_utils
    assert hasattr(data_utils, 'load_bitcoin_data')


def test_basic_import():
    """Test basic imports work."""
    import pandas as pd
    import numpy as np
    import statsforecast
    assert pd is not None
    assert np is not None
    assert statsforecast is not None


def test_backtest_4year_script_exists():
    """Test that the 4-year backtesting script exists."""
    import os
    
    script_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'experiments', 'bitcoin-prediction', 'backtest_4year.py'
    )
    assert os.path.exists(script_path), "backtest_4year.py should exist"


def test_backtest_4year_can_import():
    """Test that the 4-year backtesting script can be imported."""
    import sys
    import os
    
    # Add experiments/bitcoin-prediction to path
    bitcoin_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'experiments', 'bitcoin-prediction'
    )
    sys.path.insert(0, bitcoin_path)
    
    # Should be able to import without errors
    # (We don't run it as it takes several minutes)
    import backtest_4year
    assert hasattr(backtest_4year, 'main')
