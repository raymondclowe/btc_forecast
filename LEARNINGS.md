# Learnings

## .gitignore rules for this repo
- results/ directory is ignored
- *.png files are ignored  
- *.csv files are ignored
- These need to be overridden to commit reports/visualizations

## Running forecasts
- Scripts use StatsForecast (open source, no API key)
- trading_forecast.py - fastest, 7-day forecast (~30s)
- main.py - moderate, multiple period backtests (~1min)
- backtest_4year.py - slowest, comprehensive 4-year analysis (~2min)

## Results from live runs (2025-11-01)
- Trading Forecast: BTC ~$109,558, mostly HOLD signals (low confidence), 1 SHORT
- Main backtest: MAPE 1.54%, directional accuracy 55% (better than random)
- 4-year backtest: MAPE 1.59%, overall score 69.6/100 (⭐⭐⭐ GOOD)
- Key finding: Excellent price accuracy, moderate directional accuracy
