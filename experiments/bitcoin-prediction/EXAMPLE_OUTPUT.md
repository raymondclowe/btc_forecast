# Example Output

This document shows example outputs from running the Bitcoin prediction analysis.

## Console Output

When you run `python main.py`, you'll see output similar to:

```
================================================================================
Bitcoin Price Prediction Analysis using TimeGPT
================================================================================

Step 1: Loading Bitcoin price data...
Loaded 3650 days of Bitcoin price history
Date range: 2015-01-01 to 2025-01-01
Price range: $178.10 to $69000.00

Step 2: Defining backtesting periods...
Defined 4 backtesting periods

Step 3: Running backtesting analysis...

Analyzing period: Recent (Last 90 days)
  Date range: 2024-10-01 to 2025-01-01
  Horizon: 1 day(s)
  Generated 12 predictions
  Results saved to: results/backtest_Recent_Last_90_days.csv
  MAPE: 4.23%
  Directional Accuracy: 58.33%

Analyzing period: Mid-term (6 months ago)
  Date range: 2024-04-01 to 2024-07-01
  Horizon: 1 day(s)
  Generated 12 predictions
  Results saved to: results/backtest_Mid-term_6_months_ago.csv
  MAPE: 5.67%
  Directional Accuracy: 54.17%

Analyzing period: Bull Market (2020-2021)
  Date range: 2020-01-01 to 2021-12-31
  Horizon: 1 day(s)
  Generated 52 predictions
  Results saved to: results/backtest_Bull_Market_2020-2021.csv
  MAPE: 8.92%
  Directional Accuracy: 60.00%

Analyzing period: Bear Market (2022)
  Date range: 2022-01-01 to 2022-12-31
  Horizon: 1 day(s)
  Generated 26 predictions
  Results saved to: results/backtest_Bear_Market_2022.csv
  MAPE: 6.34%
  Directional Accuracy: 52.00%

Step 4: Generating visualizations...
  Visualizations saved for: Recent (Last 90 days)
  Visualizations saved for: Mid-term (6 months ago)
  Visualizations saved for: Bull Market (2020-2021)
  Visualizations saved for: Bear Market (2022)

Step 5: Generating comprehensive report...

================================================================================
Bitcoin Price Prediction Analysis Report
Using TimeGPT (Nixtla)
================================================================================

## Backtesting Summary

### Recent (Last 90 days)

+-----------------------+----------+
| Metric                | Value    |
+=======================+==========+
| mae                   | 1234.56  |
| rmse                  | 1567.89  |
| mape                  | 4.23     |
| median_ape            | 3.45     |
| std_error             | 987.65   |
| mean_error            | -123.45  |
| num_predictions       | 12       |
| coverage_80           | 75.00%   |
| coverage_95           | 91.67%   |
+-----------------------+----------+

### Mid-term (6 months ago)

+-----------------------+----------+
| Metric                | Value    |
+=======================+==========+
| mae                   | 1456.78  |
| rmse                  | 1789.01  |
| mape                  | 5.67     |
| median_ape            | 4.56     |
| std_error             | 1098.76  |
| mean_error            | -234.56  |
| num_predictions       | 12       |
| coverage_80           | 83.33%   |
| coverage_95           | 91.67%   |
+-----------------------+----------+

## Directional Prediction Accuracy

### Recent (Last 90 days)

+-----------------------+----------+
| Metric                | Value    |
+=======================+==========+
| accuracy              | 58.33%   |
| precision             | 62.50%   |
| recall                | 55.56%   |
| f1_score              | 58.82%   |
| total_predictions     | 12       |
| correct_predictions   | 7        |
+-----------------------+----------+

## Key Findings and Recommendations

### Findings:

1. Average MAPE across all periods: 6.29%
2. Average directional accuracy: 56.13%
3. Average 80% confidence interval coverage: 79.17%
4. Average 95% confidence interval coverage: 91.67%

### Recommendations:

1. ✓ Directional predictions show promise - can be used for trading signals
2. ✓ Price magnitude predictions are quite accurate
3. ✓ Confidence intervals are well-calibrated

### Use Cases:

- **Short-term forecasting (1-7 days)**: Best performance observed
- **Directional trading**: Use directional predictions with proper risk management
- **Risk management**: Leverage confidence intervals for position sizing
- **Trend analysis**: Combine with technical indicators for enhanced signals

================================================================================

Analysis complete! Results saved to the 'results' directory.

Step 6: Running additional horizon analysis...

Testing 7-day forecast...
  MAPE: 7.89%
  Number of predictions: 5

Testing 30-day forecast...
  MAPE: 12.34%
  Number of predictions: 2

================================================================================
Analysis complete!
Check the 'results' directory for detailed outputs.
================================================================================
```

## Generated Files

After running the analysis, the following files are created in the `results/` directory:

### CSV Files (Detailed Results)

- `backtest_Recent_Last_90_days.csv`
- `backtest_Mid-term_6_months_ago.csv`
- `backtest_Bull_Market_2020-2021.csv`
- `backtest_Bear_Market_2022.csv`
- `horizon_7_day_forecast.csv`
- `horizon_30_day_forecast.csv`

Each CSV contains columns:
- `train_start`: Start date of training window
- `train_end`: End date of training window
- `forecast_date`: Date of the forecast
- `actual`: Actual Bitcoin price
- `predicted`: Predicted Bitcoin price
- `error`: Prediction error (actual - predicted)
- `abs_error`: Absolute error
- `pct_error`: Percentage error
- `abs_pct_error`: Absolute percentage error
- `lower_80`: Lower bound of 80% confidence interval
- `upper_80`: Upper bound of 80% confidence interval
- `in_interval_80`: Whether actual falls within 80% interval
- `lower_95`: Lower bound of 95% confidence interval
- `upper_95`: Upper bound of 95% confidence interval
- `in_interval_95`: Whether actual falls within 95% interval

### Visualization Files (PNG)

For each backtesting period, three plots are generated:

1. **Forecast vs Actual**: Shows predicted vs actual prices with confidence intervals
   - `forecast_vs_actual_Recent_Last_90_days.png`
   - Example: Line plot comparing predictions to actual prices

2. **Error Distribution**: Histograms of prediction errors
   - `error_distribution_Recent_Last_90_days.png`
   - Two subplots: Absolute error and percentage error distributions

3. **Performance Over Time**: Time series of prediction accuracy
   - `performance_over_time_Recent_Last_90_days.png`
   - Shows how error metrics evolve over the backtesting period

### Summary Report

- `analysis_report.txt`: Comprehensive text report with all metrics and recommendations

## Example Interpretation

### Understanding MAPE (Mean Absolute Percentage Error)

- **MAPE < 5%**: Excellent accuracy
- **MAPE 5-10%**: Good accuracy
- **MAPE 10-20%**: Moderate accuracy
- **MAPE > 20%**: Poor accuracy (use confidence intervals)

For Bitcoin at $30,000:
- MAPE of 5% means average error of $1,500
- MAPE of 10% means average error of $3,000

### Understanding Directional Accuracy

- **Accuracy > 55%**: Statistically significant (better than random)
- **Accuracy > 60%**: Strong predictive power
- **Accuracy > 65%**: Excellent for trading signals

### Understanding Coverage

Coverage indicates how well-calibrated the confidence intervals are:
- **80% interval should capture ~80% of actual values**
- **95% interval should capture ~95% of actual values**

If coverage is too low, intervals are too narrow (overconfident).
If coverage is too high, intervals are too wide (underconfident).

## Typical Insights

From our analysis, you might discover:

1. **Short-term predictions (1-day)** are more accurate than long-term (30-day)
2. **Volatile periods** (bull/bear markets) have higher errors
3. **Directional accuracy** is often better than 55%, useful for trading
4. **Confidence intervals** provide valuable risk estimates

## Next Steps

After reviewing the results:

1. **Adjust parameters** in `main.py` for your specific needs
2. **Focus on periods** with best performance for your use case
3. **Combine predictions** with other indicators
4. **Implement risk management** using confidence intervals
5. **Backtest trading strategies** using directional signals
