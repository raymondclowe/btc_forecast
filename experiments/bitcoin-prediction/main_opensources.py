"""
Bitcoin Price Prediction Analysis using Open Source StatsForecast.
NO API KEY REQUIRED - runs completely locally.

This script performs comprehensive backtesting of Bitcoin price predictions
using StatsForecast's AutoARIMA and AutoETS models.
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_utils import load_bitcoin_data, add_derived_features
from backtesting_statsforecast import BitcoinBacktester
from analysis import BitcoinAnalyzer


def main():
    """Main analysis pipeline using open-source StatsForecast."""
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    print("=" * 80)
    print("Bitcoin Price Prediction Analysis - Open Source (StatsForecast)")
    print("NO API KEY REQUIRED")
    print("=" * 80)
    print()
    
    # Step 1: Load and prepare data
    print("Step 1: Loading Bitcoin price data...")
    df = load_bitcoin_data()
    
    print(f"✓ Loaded {len(df)} days of Bitcoin price history")
    print(f"  Date range: {df['ds'].min().date()} to {df['ds'].max().date()}")
    print(f"  Price range: ${df['y'].min():.2f} to ${df['y'].max():.2f}")
    print()
    
    # Add unique_id column required by StatsForecast
    df['unique_id'] = 'BTC'
    
    # Step 2: Initialize backtester with ensemble of models
    print("Step 2: Initializing StatsForecast models...")
    print("  Using: AutoARIMA + AutoETS (ensemble)")
    backtester = BitcoinBacktester(df, model_type='ensemble')
    analyzer = BitcoinAnalyzer(results_dir='results')
    print()
    
    # Step 3: Define backtesting periods
    print("Step 3: Running backtests across different market periods...")
    print()
    
    periods = [
        {
            'name': 'Recent Period (Last 90 days)',
            'start_date': (df['ds'].max() - timedelta(days=120)).strftime('%Y-%m-%d'),
            'end_date': df['ds'].max().strftime('%Y-%m-%d'),
            'horizon': 1,
            'window_size': 90,
            'step_size': 1,  # Daily predictions
        },
        {
            'name': 'Mid-term (6 months ago)',
            'start_date': (df['ds'].max() - timedelta(days=240)).strftime('%Y-%m-%d'),
            'end_date': (df['ds'].max() - timedelta(days=120)).strftime('%Y-%m-%d'),
            'horizon': 1,
            'window_size': 90,
            'step_size': 1,  # Daily predictions
        },
    ]
    
    all_results = {}
    all_metrics = {}
    all_directional = {}
    
    for period in periods:
        period_name = period['name']
        print(f"Analyzing: {period_name}")
        print(f"  Date range: {period['start_date']} to {period['end_date']}")
        print(f"  Horizon: {period['horizon']} day(s)")
        print(f"  Training window: {period['window_size']} days")
        
        try:
            # Run backtest
            results = backtester.backtest_period(
                start_date=period['start_date'],
                end_date=period['end_date'],
                horizon=period['horizon'],
                window_size=period['window_size'],
                step_size=period['step_size'],
                level=[80, 95]
            )
            
            if len(results) == 0:
                print(f"  ⚠ No results generated for {period_name}")
                continue
            
            # Calculate metrics
            metrics = backtester.calculate_metrics(results)
            directional = backtester.evaluate_directional_accuracy(results)
            
            # Store results
            all_results[period_name] = results
            all_metrics[period_name] = metrics
            all_directional[period_name] = directional
            
            # Save results to CSV
            results_file = f"results/backtest_{period_name.replace(' ', '_').replace('(', '').replace(')', '')}.csv"
            results.to_csv(results_file, index=False)
            print(f"  Results saved to: {results_file}")
            
            # Print quick summary
            print(f"  MAPE: {metrics['mape']:.2f}%")
            print(f"  Directional Accuracy: {directional['accuracy']:.2%}")
            print(f"  Number of predictions: {len(results)}")
            print()
            
        except Exception as e:
            print(f"  Error analyzing period: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    if len(all_results) == 0:
        print("❌ No successful backtests completed")
        return
    
    print()
    
    # Step 4: Generate visualizations
    print("Step 4: Generating visualizations...")
    
    for period_name, results in all_results.items():
        safe_name = period_name.replace(' ', '_').replace('(', '').replace(')', '')
        
        # Plot forecast vs actual
        try:
            fig1 = analyzer.plot_forecast_vs_actual(
                results,
                title=f"Bitcoin Price Forecast vs Actual - {period_name}",
                save_path=f"results/forecast_vs_actual_{safe_name}.png"
            )
            plt.close(fig1)
        except Exception as e:
            print(f"  Error creating forecast plot: {e}")
        
        # Plot error distribution
        try:
            fig2 = analyzer.plot_error_distribution(
                results,
                title=f"Forecast Error Distribution - {period_name}",
                save_path=f"results/error_distribution_{safe_name}.png"
            )
            plt.close(fig2)
        except Exception as e:
            print(f"  Error creating error distribution: {e}")
        
        # Plot simple performance summary
        try:
            fig3 = analyzer.plot_simple_performance_summary(
                results,
                save_path=f"results/simple_summary_{safe_name}.png"
            )
            plt.close(fig3)
        except Exception as e:
            print(f"  Error creating simple summary: {e}")
        
        print(f"  Visualizations saved for: {period_name}")
    
    print()
    
    # Step 5: Generate performance scorecard
    print("Step 5: Generating performance scorecard...")
    try:
        scorecard_fig = analyzer.plot_accuracy_scorecard(
            all_metrics,
            all_directional,
            save_path='results/performance_scorecard.png'
        )
        plt.close(scorecard_fig)
        print("  ✓ Performance scorecard saved to: results/performance_scorecard.png")
    except Exception as e:
        print(f"  Error creating scorecard: {e}")
    
    print()
    
    # Step 6: Generate comprehensive report
    print("Step 6: Generating comprehensive report...")
    
    report = analyzer.generate_summary_report(
        all_metrics,
        all_directional,
        save_path='results/analysis_report.txt'
    )
    
    print("\n" + report)
    
    print()
    print("=" * 80)
    print("Analysis complete! Results saved to the 'results' directory.")
    print()
    print("REAL RESULTS - No simulation, actual Bitcoin data with StatsForecast")
    print()
    print("Summary of Findings:")
    print("-" * 80)
    
    for period_name in all_metrics.keys():
        metrics = all_metrics[period_name]
        directional = all_directional[period_name]
        
        print(f"\n{period_name}:")
        print(f"  MAPE: {metrics['mape']:.2f}%")
        print(f"  MAE: ${metrics['mae']:.2f}")
        print(f"  Directional Accuracy: {directional['accuracy']:.1%}")
        
        if directional['accuracy'] > 0.50:
            print(f"  ✓ Better than random (50%)")
        else:
            print(f"  ⚠ Not better than random")
        
        if metrics['mape'] < 10:
            print(f"  ✓ Excellent price accuracy (<10% MAPE)")
        elif metrics['mape'] < 20:
            print(f"  ~ Good price accuracy (<20% MAPE)")
        else:
            print(f"  ⚠ Moderate accuracy (>{metrics['mape']:.0f}% MAPE)")
    
    print("\n" + "=" * 80)


if __name__ == '__main__':
    main()
