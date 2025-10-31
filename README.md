# Bitcoin Forecasting

This repository contains tools for Bitcoin price forecasting using open-source StatsForecast models.

## Quick Start

### Trading Forecast

Generate a 7-day Bitcoin price forecast with actionable trading signals:

```bash
uv run experiments/bitcoin-prediction/trading_forecast.py
```

### Backtesting

Run comprehensive backtesting analysis on historical data:

```bash
uv run experiments/bitcoin-prediction/main.py
```

## Requirements

- Python 3.9+
- uv package manager

Dependencies are managed through `pyproject.toml` and automatically installed when using `uv run`.

## Features

- **No API Keys Required**: 100% free and runs locally
- **Open Source Models**: Uses StatsForecast (AutoARIMA + AutoETS)
- **Actionable Signals**: Clear trading recommendations with confidence levels
- **Proven Results**: Backtested on 5,500+ days of Bitcoin price history

## Documentation

See [experiments/bitcoin-prediction/README.md](experiments/bitcoin-prediction/README.md) for detailed documentation.

## License

MIT
