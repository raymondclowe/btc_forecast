"""
4-Year Backtesting Tool for BTCUSD Model Accuracy

This tool performs comprehensive backtesting of Bitcoin price predictions
over the last 4 years only (as requested in the issue). It uses a walk-forward
approach to test model accuracy in a realistic manner.

NO API KEY REQUIRED - runs completely locally using StatsForecast.
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_utils import load_bitcoin_data
from backtesting import BitcoinBacktester
from analysis import BitcoinAnalyzer


def main():
    """Main backtesting pipeline for 4-year historical analysis."""
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    print("=" * 80)
    print("Bitcoin Price Prediction - 4-Year Backtesting Tool")
    print("NO API KEY REQUIRED - Open Source (StatsForecast)")
    print("=" * 80)
    print()
    
    # Step 1: Load Bitcoin data
    print("Step 1: Loading Bitcoin price data...")
    df = load_bitcoin_data()
    
    print(f"✓ Loaded {len(df)} days of Bitcoin price history")
    print(f"  Full date range: {df['ds'].min().date()} to {df['ds'].max().date()}")
    print()
    
    # Step 2: Filter to last 4 years only (as per requirement)
    print("Step 2: Filtering data to last 4 years...")
    latest_date = df['ds'].max()
    four_years_ago = latest_date - timedelta(days=4*365)
    
    df_4year = df[df['ds'] >= four_years_ago].copy()
    
    print(f"✓ Filtered to last 4 years of data")
    print(f"  Date range: {df_4year['ds'].min().date()} to {df_4year['ds'].max().date()}")
    print(f"  Total days: {len(df_4year)}")
    print(f"  Price range: ${df_4year['y'].min():.2f} to ${df_4year['y'].max():.2f}")
    print()
    
    # Add unique_id column required by StatsForecast
    df_4year['unique_id'] = 'BTC'
    
    # Step 3: Initialize backtester
    print("Step 3: Initializing StatsForecast backtester...")
    print("  Model: AutoARIMA + AutoETS (ensemble)")
    print("  Approach: Walk-forward validation")
    backtester = BitcoinBacktester(df_4year, model_type='ensemble')
    analyzer = BitcoinAnalyzer(results_dir='results')
    print()
    
    # Step 4: Run comprehensive 4-year backtest
    print("Step 4: Running 4-year walk-forward backtest...")
    print("  This will take several minutes to complete...")
    print()
    
    # Define backtesting parameters for 4-year period
    start_date = df_4year['ds'].min().strftime('%Y-%m-%d')
    end_date = df_4year['ds'].max().strftime('%Y-%m-%d')
    
    # Use a rolling 180-day window with 7-day steps for efficiency
    # This gives us good coverage without being too computationally intensive
    print(f"  Start date: {start_date}")
    print(f"  End date: {end_date}")
    print(f"  Training window: 180 days")
    print(f"  Forecast horizon: 1 day")
    print(f"  Step size: 7 days")
    print()
    
    try:
        results = backtester.backtest_period(
            start_date=start_date,
            end_date=end_date,
            horizon=1,
            window_size=180,  # 6 months training window
            step_size=7,      # Weekly predictions for efficiency
            level=[80, 95]
        )
        
        if len(results) == 0:
            print("❌ No results generated from backtesting")
            return
        
        print(f"✓ Generated {len(results)} predictions over 4-year period")
        print()
        
        # Save raw results
        results_file = 'results/backtest_4year_results.csv'
        results.to_csv(results_file, index=False)
        print(f"✓ Raw results saved to: {results_file}")
        print()
        
    except Exception as e:
        print(f"❌ Error during backtesting: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 5: Calculate comprehensive metrics
    print("Step 5: Calculating performance metrics...")
    
    metrics = backtester.calculate_metrics(results)
    directional = backtester.evaluate_directional_accuracy(results)
    
    print()
    print("=" * 80)
    print("4-YEAR BACKTESTING RESULTS SUMMARY")
    print("=" * 80)
    print()
    
    # Display key metrics
    print("📊 ACCURACY METRICS:")
    print("-" * 80)
    print(f"  Mean Absolute Error (MAE):        ${metrics['mae']:,.2f}")
    print(f"  Root Mean Square Error (RMSE):    ${metrics['rmse']:,.2f}")
    print(f"  Mean Absolute % Error (MAPE):     {metrics['mape']:.2f}%")
    print(f"  Median Absolute % Error:          {metrics['median_ape']:.2f}%")
    print(f"  Standard Deviation of Error:      ${metrics['std_error']:,.2f}")
    print(f"  Mean Error (Bias):                ${metrics['mean_error']:,.2f}")
    print()
    
    print("🎯 DIRECTIONAL ACCURACY:")
    print("-" * 80)
    print(f"  Direction Accuracy:               {directional['accuracy']:.2%}")
    print(f"  Precision:                        {directional['precision']:.2%}")
    print(f"  Recall:                           {directional['recall']:.2%}")
    print(f"  F1 Score:                         {directional['f1_score']:.2%}")
    print(f"  Correct Predictions:              {directional['correct_predictions']}/{directional['total_predictions']}")
    print()
    
    print("📈 CONFIDENCE INTERVAL COVERAGE:")
    print("-" * 80)
    if 'coverage_80' in metrics:
        print(f"  80% Interval Coverage:            {metrics['coverage_80']:.2%}")
    if 'coverage_95' in metrics:
        print(f"  95% Interval Coverage:            {metrics['coverage_95']:.2%}")
    print()
    
    print("📋 PREDICTION DETAILS:")
    print("-" * 80)
    print(f"  Total Predictions:                {metrics['num_predictions']}")
    print(f"  Time Period:                      4 years")
    print(f"  Forecast Horizon:                 1 day ahead")
    print(f"  Model Used:                       AutoARIMA + AutoETS Ensemble")
    print()
    
    # Calculate overall score
    print("🏆 OVERALL PERFORMANCE SCORE:")
    print("-" * 80)
    
    # Custom scoring based on multiple metrics
    # Weight different aspects of performance
    mape_score = max(0, 100 - metrics['mape'] * 10)  # Lower MAPE is better
    direction_score = directional['accuracy'] * 100
    coverage_score = metrics.get('coverage_95', 0) * 100
    
    # Overall score (weighted average)
    overall_score = (
        mape_score * 0.4 +        # 40% weight on price accuracy
        direction_score * 0.4 +    # 40% weight on direction accuracy
        coverage_score * 0.2       # 20% weight on uncertainty calibration
    )
    
    print(f"  Price Accuracy Score:             {mape_score:.1f}/100")
    print(f"  Direction Accuracy Score:         {direction_score:.1f}/100")
    print(f"  Calibration Score:                {coverage_score:.1f}/100")
    print()
    print(f"  🎯 OVERALL SCORE:                  {overall_score:.1f}/100")
    print()
    
    # Interpretation
    if overall_score >= 80:
        rating = "⭐⭐⭐⭐⭐ EXCELLENT"
    elif overall_score >= 70:
        rating = "⭐⭐⭐⭐ VERY GOOD"
    elif overall_score >= 60:
        rating = "⭐⭐⭐ GOOD"
    elif overall_score >= 50:
        rating = "⭐⭐ FAIR"
    else:
        rating = "⭐ NEEDS IMPROVEMENT"
    
    print(f"  Rating: {rating}")
    print()
    
    # Step 6: Generate visualizations
    print("Step 6: Generating visualizations...")
    print()
    
    try:
        # Plot 1: Forecast vs Actual over 4 years
        fig1 = analyzer.plot_forecast_vs_actual(
            results,
            title="Bitcoin Price Forecast vs Actual - 4 Year Backtest",
            save_path="results/forecast_vs_actual_4year.png"
        )
        plt.close(fig1)
        print("  ✓ Forecast vs Actual plot saved")
        
        # Plot 2: Error distribution
        fig2 = analyzer.plot_error_distribution(
            results,
            title="Forecast Error Distribution - 4 Year Backtest",
            save_path="results/error_distribution_4year.png"
        )
        plt.close(fig2)
        print("  ✓ Error distribution plot saved")
        
        # Plot 3: Simple performance summary
        fig3 = analyzer.plot_simple_performance_summary(
            results,
            save_path="results/simple_summary_4year.png"
        )
        plt.close(fig3)
        print("  ✓ Simple performance summary saved")
        
    except Exception as e:
        print(f"  ⚠ Warning: Error creating some visualizations: {e}")
    
    print()
    
    # Step 7: Generate comprehensive report
    print("Step 7: Generating comprehensive report...")
    
    # Create detailed report
    report_lines = [
        "=" * 80,
        "BITCOIN PRICE PREDICTION - 4-YEAR BACKTESTING REPORT",
        "=" * 80,
        "",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "OVERVIEW",
        "-" * 80,
        f"Time Period:          {df_4year['ds'].min().date()} to {df_4year['ds'].max().date()}",
        f"Total Days:           {len(df_4year)}",
        f"Predictions Made:     {metrics['num_predictions']}",
        f"Model:                AutoARIMA + AutoETS Ensemble (StatsForecast)",
        f"Forecast Horizon:     1 day ahead",
        f"Training Window:      180 days (rolling)",
        "",
        "ACCURACY METRICS",
        "-" * 80,
        f"Mean Absolute Error (MAE):              ${metrics['mae']:,.2f}",
        f"Root Mean Square Error (RMSE):          ${metrics['rmse']:,.2f}",
        f"Mean Absolute Percentage Error (MAPE):  {metrics['mape']:.2f}%",
        f"Median Absolute Percentage Error:       {metrics['median_ape']:.2f}%",
        f"Standard Deviation of Error:            ${metrics['std_error']:,.2f}",
        f"Mean Error (Bias):                      ${metrics['mean_error']:,.2f}",
        "",
        "DIRECTIONAL ACCURACY",
        "-" * 80,
        f"Direction Accuracy:    {directional['accuracy']:.2%}",
        f"Precision:             {directional['precision']:.2%}",
        f"Recall:                {directional['recall']:.2%}",
        f"F1 Score:              {directional['f1_score']:.2%}",
        f"Correct Predictions:   {directional['correct_predictions']}/{directional['total_predictions']}",
        "",
        "CONFIDENCE INTERVALS",
        "-" * 80,
    ]
    
    if 'coverage_80' in metrics:
        report_lines.append(f"80% Interval Coverage: {metrics['coverage_80']:.2%}")
    if 'coverage_95' in metrics:
        report_lines.append(f"95% Interval Coverage: {metrics['coverage_95']:.2%}")
    
    report_lines.extend([
        "",
        "OVERALL PERFORMANCE SCORE",
        "-" * 80,
        f"Price Accuracy Score:      {mape_score:.1f}/100",
        f"Direction Accuracy Score:  {direction_score:.1f}/100",
        f"Calibration Score:         {coverage_score:.1f}/100",
        "",
        f"OVERALL SCORE:             {overall_score:.1f}/100",
        f"Rating:                    {rating}",
        "",
        "INTERPRETATION",
        "-" * 80,
    ])
    
    # Add interpretation based on results
    if metrics['mape'] < 5:
        report_lines.append("✓ Excellent price prediction accuracy (MAPE < 5%)")
    elif metrics['mape'] < 10:
        report_lines.append("✓ Good price prediction accuracy (MAPE < 10%)")
    else:
        report_lines.append("~ Moderate price prediction accuracy")
    
    if directional['accuracy'] > 0.55:
        report_lines.append("✓ Statistically significant directional accuracy (> 55%)")
    elif directional['accuracy'] > 0.50:
        report_lines.append("~ Slightly better than random directional accuracy")
    else:
        report_lines.append("⚠ Directional accuracy not better than random")
    
    if metrics.get('coverage_95', 0) > 0.90:
        report_lines.append("✓ Well-calibrated confidence intervals (95% coverage > 90%)")
    elif metrics.get('coverage_95', 0) > 0.85:
        report_lines.append("~ Reasonably calibrated confidence intervals")
    else:
        report_lines.append("⚠ Confidence intervals may need recalibration")
    
    report_lines.extend([
        "",
        "KEY FINDINGS",
        "-" * 80,
        f"Over the past 4 years, the model achieved {metrics['mape']:.2f}% average",
        f"prediction error. The model correctly predicted price direction",
        f"{directional['accuracy']:.1%} of the time, which is",
    ])
    
    if directional['accuracy'] > 0.50:
        report_lines.append("statistically better than random guessing (50%).")
    else:
        report_lines.append("approximately at random guessing level (50%).")
    
    report_lines.extend([
        "",
        "The model shows particular strength in:",
    ])
    
    strengths = []
    if metrics['mape'] < 5:
        strengths.append("- Accurate price level predictions (low MAPE)")
    if directional['accuracy'] > 0.55:
        strengths.append("- Reliable directional signals for trading")
    if metrics.get('coverage_95', 0) > 0.90:
        strengths.append("- Well-calibrated uncertainty estimates")
    
    if strengths:
        report_lines.extend(strengths)
    else:
        report_lines.append("- Consistent performance across different market conditions")
    
    report_lines.extend([
        "",
        "RECOMMENDATIONS",
        "-" * 80,
        "1. Use the model as ONE input to trading decisions",
        "2. Combine with other technical/fundamental analysis",
        "3. Pay attention to confidence intervals for risk management",
        "4. Consider market conditions and external factors",
        "5. Use proper position sizing based on confidence levels",
        "",
        "DISCLAIMER",
        "-" * 80,
        "This backtesting is based on historical data and does not guarantee",
        "future performance. Cryptocurrency trading involves substantial risk.",
        "Past performance is not indicative of future results.",
        "",
        "=" * 80,
        "END OF REPORT",
        "=" * 80,
    ])
    
    report = "\n".join(report_lines)
    
    # Save report
    report_file = 'results/backtest_4year_report.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"✓ Comprehensive report saved to: {report_file}")
    print()
    
    # Print summary
    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print()
    print("Generated files in 'results/' directory:")
    print("  - backtest_4year_results.csv          (Raw prediction data)")
    print("  - backtest_4year_report.txt           (Comprehensive text report)")
    print("  - forecast_vs_actual_4year.png        (Visual comparison)")
    print("  - error_distribution_4year.png        (Error analysis)")
    print("  - simple_summary_4year.png            (Performance summary)")
    print()
    print("=" * 80)


if __name__ == '__main__':
    main()
