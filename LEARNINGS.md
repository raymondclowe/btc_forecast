# Learnings

## .gitignore rules for this repo
- results/ directory is ignored
- *.png files are ignored  
- *.csv files are ignored
- These need to be overridden to commit reports/visualizations

## Running forecasts
- Scripts use StatsForecast (open source, no API key)
- trading_forecast.py - fastest, 7-day forecast
- main.py - moderate, multiple period backtests  
- backtest_4year.py - slowest, comprehensive 4-year analysis
