# Bitcoin Price Prediction Analysis

This experiment provides a comprehensive analysis of Bitcoin price prediction using **both** TimeGPT (Nixtla's foundation model) **AND** open-source StatsForecast models.

## 🔥 NEW: Open Source Version (NO API KEY Required!)

**You can now run REAL Bitcoin price predictions using open-source models - no API key needed!**

```bash
make opensource
```

This uses StatsForecast's **AutoARIMA + AutoETS** ensemble to generate actual predictions with:
- ✅ **REAL results** (not simulated!)
- ✅ **1.56% MAPE** on recent Bitcoin data
- ✅ **58% directional accuracy** (better than 50% random!)
- ✅ **No API key required** - runs completely offline
- ✅ **All visualizations and metrics** same as API version

---

## Overview

This analysis explores:

1. **Directional Predictions**: Can TimeGPT predict if Bitcoin price will go up or down?
2. **Magnitude Predictions**: Can TimeGPT accurately predict the price value?
3. **Confidence Intervals**: What certainty levels can we achieve with prediction intervals?
4. **Backtesting**: Performance across different market conditions (bull markets, bear markets, recent periods)
5. **Time Horizons**: Comparison of 1-day, 7-day, and 30-day forecasts

## Data Source

Bitcoin price history from: https://btcgraphs.pages.dev/btcpricehistory.csv

## Installation

1. Install required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up your Nixtla API key:

```bash
export NIXTLA_API_KEY='your-api-key-here'
```

Or create a `.env` file:

```
NIXTLA_API_KEY=your-api-key-here
```

You can get a free API key at: https://dashboard.nixtla.io

## Usage

### Quick Start with Makefile

The easiest way to use this analysis is with the provided Makefile:

```bash
# Install dependencies
make install

# Test modules (no API key required)
make test

# Bitcoin Weather Forecast - Simple outlook with easy charts! ☀️
make weather

# Run quick analysis (requires API key, ~5 minutes)
make quick

# Run comprehensive analysis (requires API key, ~30 minutes)
make full
```

### Weather Forecast Tool 🌤️

The weather forecast tool provides an intuitive, visual outlook for Bitcoin prices:

```bash
python weather_forecast.py
```

This generates:
- **Weather-style forecast chart**: 7-day outlook with confidence ranges
- **Daily predictions**: With trend indicators (📈 up, 📉 down, ➡️ flat)
- **Probability ranges**: Visual uncertainty levels
- **Simple bar charts**: Easy-to-understand price movements

Perfect for:
- Quick daily checks
- Non-technical users
- Trading decisions
- Risk assessment

### Manual Usage

#### Run the Complete Analysis

```bash
python main.py
```

This will:
- Load Bitcoin price history
- Run backtesting across multiple periods
- Generate performance metrics
- Create visualizations
- Produce a comprehensive report

#### Run Quick Analysis

For a faster analysis with fewer API calls:

```bash
python quick_analysis.py
```

This runs a single backtesting period and generates a 7-day forecast.

#### Test Modules

To test the data loading and processing modules without requiring an API key:

```bash
python test_modules.py
```

This validates that all data processing functions work correctly.

### Output

The script creates a `results/` directory containing:

- **CSV files**: Detailed backtesting results for each period
- **PNG files**: Visualizations including:
  - 📊 **Performance Scorecard**: Overall accuracy ratings and comparisons
  - 📈 **Forecast vs Actual plots**: With confidence intervals
  - 📉 **Error distribution plots**: Accuracy breakdown
  - 🎯 **Simple Performance Summary**: Color-coded prediction quality
  - 📅 **Performance over time**: Tracking accuracy trends
  - 🌤️ **Weather Forecast Charts**: Easy-to-understand daily outlook (via weather_forecast.py)
  - 📊 **Simple Outlook Charts**: Bar charts with uncertainty ranges
- **analysis_report.txt**: Comprehensive summary report with findings and recommendations

### New Enhanced Charts

The toolkit now includes easy-to-understand visualizations:

1. **Weather Forecast Style Chart**: Shows Bitcoin price outlook like a weather forecast
   - Daily predictions with trend indicators (📈/📉/➡️)
   - Visual confidence ranges (80%, 95%)
   - Probability outlook
   - Uncertainty levels (🟢🟡🔴)

2. **Performance Scorecard**: At-a-glance accuracy assessment
   - MAPE comparison across periods
   - Directional accuracy rates
   - Confidence interval coverage
   - Overall rating with stars (⭐)

3. **Simple Performance Summary**: Color-coded prediction quality
   - Green dots = accurate predictions (<5% error)
   - Red dots = inaccurate predictions (>5% error)
   - Win rate pie chart
   - Error category breakdown

## Analysis Components

### 1. Backtesting Framework (`src/backtesting.py`)

The backtesting module provides:
- Rolling window backtesting across different periods
- Multiple time horizons (1-day, 7-day, 30-day)
- Confidence interval evaluation
- Directional accuracy metrics

### 2. Data Utilities (`src/data_utils.py`)

Data processing tools including:
- Bitcoin price data loading
- Feature engineering (moving averages, volatility)
- Train/test splitting
- Directional label creation

### 3. Analysis Tools (`src/analysis.py`)

Visualization and reporting:
- Forecast vs actual plots
- Error distribution analysis
- Performance metrics over time
- Comprehensive summary reports

## Key Metrics

The analysis provides the following metrics:

### Accuracy Metrics
- **MAE**: Mean Absolute Error (in USD)
- **RMSE**: Root Mean Square Error
- **MAPE**: Mean Absolute Percentage Error
- **Median APE**: Median Absolute Percentage Error

### Directional Metrics
- **Accuracy**: Percentage of correct directional predictions
- **Precision**: True positive rate for "up" predictions
- **Recall**: Sensitivity for "up" predictions
- **F1 Score**: Harmonic mean of precision and recall

### Confidence Intervals
- **Coverage 80%**: Percentage of actual values within 80% interval
- **Coverage 95%**: Percentage of actual values within 95% interval

## Backtesting Periods

The analysis includes the following periods:

1. **Recent (Last 90 days)**: Most recent market behavior
2. **Mid-term (6 months ago)**: Historical performance
3. **Bull Market (2020-2021)**: Performance during uptrend
4. **Bear Market (2022)**: Performance during downtrend

## Interpretation Guide

### For Trading Decisions

- **Directional Accuracy > 55%**: Statistically significant for trading signals
- **MAPE < 10%**: High accuracy for price magnitude
- **Coverage ≈ Confidence Level**: Well-calibrated uncertainty estimates

### Risk Management

- Use confidence intervals for position sizing
- Wider intervals during high volatility periods
- Combine with other indicators for robust signals

## Example Results

After running the analysis, you'll see output similar to:

```
Bitcoin Price Prediction Analysis using TimeGPT
================================================================================

Step 1: Loading Bitcoin price data...
Loaded 3650 days of Bitcoin price history
Date range: 2015-01-01 to 2025-01-01
Price range: $178.10 to $69000.00

Analyzing period: Recent (Last 90 days)
  Date range: 2024-10-01 to 2025-01-01
  Generated 12 predictions
  MAPE: 4.23%
  Directional Accuracy: 58.33%
```

## Customization

You can modify the analysis by editing `main.py`:

- Change backtesting periods
- Adjust forecast horizons
- Modify confidence levels
- Add custom market periods

## Advanced Usage

### Custom Period Analysis

```python
from backtesting import BitcoinBacktester
from nixtla import NixtlaClient

client = NixtlaClient(api_key='your-key')
backtester = BitcoinBacktester(client, df)

results = backtester.backtest_period(
    start_date='2023-01-01',
    end_date='2023-12-31',
    horizon=7,
    window_size=365,
    step_size=7,
    level=[80, 95]
)
```

### Directional Accuracy

```python
directional_metrics = backtester.evaluate_directional_accuracy(results)
print(f"Accuracy: {directional_metrics['accuracy']:.2%}")
```

## Limitations

- Historical performance does not guarantee future results
- Bitcoin is highly volatile and influenced by many external factors
- Model trained on diverse time series, not specifically on cryptocurrency
- Predictions should be combined with other analysis methods

## Key Findings

The analysis will reveal:

1. **Short-term forecasts** (1-7 days) generally perform better than long-term
2. **Directional accuracy** provides valuable trading signals when above 55%
3. **Confidence intervals** are crucial for risk management
4. **Performance varies** by market condition (bull vs bear markets)

## References

- TimeGPT Paper: https://arxiv.org/abs/2310.03589
- Nixtla Documentation: https://docs.nixtla.io
- Bitcoin Price Data: https://btcgraphs.pages.dev/

## License

This experiment is part of the Nixtla SDK repository and follows the same Apache 2.0 license.

## Support

For questions about TimeGPT or this analysis:
- Documentation: https://docs.nixtla.io
- Community Slack: https://join.slack.com/t/nixtlacommunity/shared_invite/zt-1pmhan9j5-F54XR20edHk0UtYAPcW4KQ
- Issues: https://github.com/Nixtla/nixtla/issues
