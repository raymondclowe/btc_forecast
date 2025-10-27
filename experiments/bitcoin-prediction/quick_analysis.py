"""
Quick Bitcoin Price Prediction Analysis.

This script runs a simplified analysis with fewer periods for faster results.
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from nixtla import NixtlaClient
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_utils import load_bitcoin_data, add_derived_features
from backtesting import BitcoinBacktester
from analysis import BitcoinAnalyzer


def main():
    """Quick analysis pipeline."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize client
    api_key = os.environ.get('NIXTLA_API_KEY')
    if not api_key:
        print("Error: NIXTLA_API_KEY not found in environment.")
        print("Set your API key with: export NIXTLA_API_KEY='your-key-here'")
        return
    
    client = NixtlaClient(api_key=api_key)
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    print("=" * 80)
    print("Bitcoin Price Prediction - Quick Analysis")
    print("=" * 80)
    print()
    
    # Load data
    print("Loading Bitcoin price data...")
    df = load_bitcoin_data()
    print(f"✓ Loaded {len(df)} days of Bitcoin price history")
    print(f"  Date range: {df['ds'].min().date()} to {df['ds'].max().date()}")
    print()
    
    # Initialize tools
    backtester = BitcoinBacktester(client, df)
    analyzer = BitcoinAnalyzer(results_dir='results')
    
    # Run a single recent analysis
    max_date = df['ds'].max()
    start_date = (max_date - timedelta(days=60)).strftime('%Y-%m-%d')
    end_date = max_date.strftime('%Y-%m-%d')
    
    print(f"Running quick backtest: {start_date} to {end_date}")
    print("Using 1-day forecast horizon with 90-day training window")
    print()
    
    try:
        # Run backtest with smaller window
        results = backtester.backtest_period(
            start_date=start_date,
            end_date=end_date,
            horizon=1,
            window_size=90,
            step_size=7,
            level=[80, 95]
        )
        
        if len(results) == 0:
            print("✗ No results generated (insufficient data)")
            return
        
        print(f"✓ Generated {len(results)} predictions")
        print()
        
        # Calculate metrics
        print("Performance Metrics:")
        metrics = backtester.calculate_metrics(results)
        directional = backtester.evaluate_directional_accuracy(results)
        
        print(f"  MAE: ${metrics['mae']:.2f}")
        print(f"  RMSE: ${metrics['rmse']:.2f}")
        print(f"  MAPE: {metrics['mape']:.2f}%")
        print(f"  80% Confidence Coverage: {metrics.get('coverage_80', 0):.1%}")
        print(f"  95% Confidence Coverage: {metrics.get('coverage_95', 0):.1%}")
        print()
        
        print("Directional Accuracy:")
        print(f"  Accuracy: {directional['accuracy']:.1%}")
        print(f"  Precision: {directional['precision']:.1%}")
        print(f"  Recall: {directional['recall']:.1%}")
        print(f"  F1 Score: {directional['f1_score']:.1%}")
        print()
        
        # Save results
        results.to_csv('results/quick_analysis.csv', index=False)
        print("✓ Results saved to: results/quick_analysis.csv")
        
        # Generate visualizations
        print("\nGenerating visualizations...")
        
        fig1 = analyzer.plot_forecast_vs_actual(
            results,
            title="Bitcoin Price: Forecast vs Actual",
            save_path='results/quick_forecast_vs_actual.png'
        )
        plt.close(fig1)
        print("✓ Saved: results/quick_forecast_vs_actual.png")
        
        fig2 = analyzer.plot_error_distribution(
            results,
            title="Forecast Error Distribution",
            save_path='results/quick_error_distribution.png'
        )
        plt.close(fig2)
        print("✓ Saved: results/quick_error_distribution.png")
        
        # NEW: Add simple performance summary
        print("Creating simple performance summary...")
        fig3 = analyzer.plot_simple_performance_summary(
            results,
            save_path='results/quick_simple_summary.png'
        )
        plt.close(fig3)
        print("✓ Saved: results/quick_simple_summary.png")
        
        # Test a simple forecast
        print("\nTesting simple 7-day forecast...")
        
        # Use last 180 days for training
        train_df = df.tail(180).copy()
        
        forecast = client.forecast(
            df=train_df,
            h=7,
            level=[80, 95]
        )
        
        print(f"✓ Forecast generated for next 7 days")
        print("\nForecast (next 7 days):")
        print(forecast[['ds', 'TimeGPT', 'TimeGPT-lo-80', 'TimeGPT-hi-80']].to_string(index=False))
        
        forecast.to_csv('results/quick_forecast_7days.csv', index=False)
        print("\n✓ Forecast saved to: results/quick_forecast_7days.csv")
        
        print()
        print("=" * 80)
        print("Quick analysis complete!")
        print()
        print("Key Findings:")
        
        if directional['accuracy'] > 0.55:
            print("  ✓ Directional predictions show promise (better than random)")
        else:
            print("  ⚠ Directional accuracy near random - use with caution")
        
        if metrics['mape'] < 10:
            print("  ✓ Price predictions are quite accurate (MAPE < 10%)")
        elif metrics['mape'] < 20:
            print("  ~ Price predictions are moderately accurate (MAPE < 20%)")
        else:
            print("  ⚠ High prediction error - focus on confidence intervals")
        
        coverage_ok = metrics.get('coverage_80', 0) > 0.70 and metrics.get('coverage_95', 0) > 0.85
        if coverage_ok:
            print("  ✓ Confidence intervals are well-calibrated")
        else:
            print("  ⚠ Confidence intervals may need adjustment")
        
        print()
        print("For comprehensive analysis, run: python main.py")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
