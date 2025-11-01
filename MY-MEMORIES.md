# My Memories

## Current Task
- Working on issue: "Live and commit reports and graphs"
- Goal: Run forecasting tools with real data, commit/push reports and visualizations
- Branch: copilot/live-reports-and-graphs

## What I Know
- Repo has 3 main scripts:
  1. trading_forecast.py - Daily 7-day trading signals
  2. main.py - Backtesting analysis
  3. backtest_4year.py - 4-year historical analysis
- Uses StatsForecast (AutoARIMA + AutoETS) - NO API KEY needed
- Results go to results/ directory (currently doesn't exist)
- CSV/PNG files are gitignored but need to commit them for this issue
- Need to modify .gitignore to allow committing outputs

## Status
- Modified .gitignore files to allow committing outputs
- Completed all 3 live runs:
  1. trading_forecast.py - 7-day forecast with trading signals
  2. main.py - Recent + Mid-term backtests with visualizations
  3. backtest_4year.py - Comprehensive 4-year analysis
- Generated 19 files (CSVs, PNGs, TXTs)
- Ready to commit all results
