"""
Bitcoin Price Prediction Analysis using TimeGPT.

This script performs comprehensive analysis of Bitcoin price predictions,
including backtesting across different periods, directional accuracy,
and magnitude predictions with confidence intervals.
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
    """Main analysis pipeline."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize client
    api_key = os.environ.get('NIXTLA_API_KEY')
    if not api_key:
        print("Warning: NIXTLA_API_KEY not found in environment.")
        print("Set your API key with: export NIXTLA_API_KEY='your-key-here'")
        print("Or create a .env file with: NIXTLA_API_KEY=your-key-here")
        return
    
    client = NixtlaClient(api_key=api_key)
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    print("=" * 80)
    print("Bitcoin Price Prediction Analysis using TimeGPT")
    print("=" * 80)
    print()
    
    # Step 1: Load data
    print("Step 1: Loading Bitcoin price data...")
    df = load_bitcoin_data()
    print(f"Loaded {len(df)} days of Bitcoin price history")
    print(f"Date range: {df['ds'].min()} to {df['ds'].max()}")
    print(f"Price range: ${df['y'].min():.2f} to ${df['y'].max():.2f}")
    print()
    
    # Step 2: Define backtesting periods
    print("Step 2: Defining backtesting periods...")
    
    # Get the most recent data date
    max_date = df['ds'].max()
    
    # Define different test periods
    periods = {
        'Recent (Last 90 days)': {
            'start_date': (max_date - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end_date': max_date.strftime('%Y-%m-%d'),
            'horizon': 1,
            'window_size': 180,
            'step_size': 7
        },
        'Mid-term (6 months ago)': {
            'start_date': (max_date - timedelta(days=270)).strftime('%Y-%m-%d'),
            'end_date': (max_date - timedelta(days=180)).strftime('%Y-%m-%d'),
            'horizon': 1,
            'window_size': 180,
            'step_size': 7
        },
        'Bull Market (2020-2021)': {
            'start_date': '2020-01-01',
            'end_date': '2021-12-31',
            'horizon': 1,
            'window_size': 180,
            'step_size': 14
        },
        'Bear Market (2022)': {
            'start_date': '2022-01-01',
            'end_date': '2022-12-31',
            'horizon': 1,
            'window_size': 180,
            'step_size': 14
        }
    }
    
    print(f"Defined {len(periods)} backtesting periods")
    print()
    
    # Step 3: Run backtesting
    print("Step 3: Running backtesting analysis...")
    backtester = BitcoinBacktester(client, df)
    analyzer = BitcoinAnalyzer(results_dir='results')
    
    all_results = {}
    all_metrics = {}
    all_directional = {}
    
    for period_name, config in periods.items():
        print(f"\nAnalyzing period: {period_name}")
        print(f"  Date range: {config['start_date']} to {config['end_date']}")
        print(f"  Horizon: {config['horizon']} day(s)")
        
        try:
            # Run backtest
            results = backtester.backtest_period(
                start_date=config['start_date'],
                end_date=config['end_date'],
                horizon=config['horizon'],
                window_size=config['window_size'],
                step_size=config['step_size'],
                level=[80, 95]
            )
            
            if len(results) == 0:
                print(f"  No results for this period (insufficient data)")
                continue
            
            print(f"  Generated {len(results)} predictions")
            
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
            
        except Exception as e:
            print(f"  Error analyzing period: {e}")
            continue
    
    print()
    
    # Step 4: Generate visualizations
    print("Step 4: Generating visualizations...")
    
    for period_name, results in all_results.items():
        safe_name = period_name.replace(' ', '_').replace('(', '').replace(')', '')
        
        # Plot forecast vs actual
        fig1 = analyzer.plot_forecast_vs_actual(
            results,
            title=f"Bitcoin Price Forecast vs Actual - {period_name}",
            save_path=f"results/forecast_vs_actual_{safe_name}.png"
        )
        plt.close(fig1)
        
        # Plot error distribution
        fig2 = analyzer.plot_error_distribution(
            results,
            title=f"Forecast Error Distribution - {period_name}",
            save_path=f"results/error_distribution_{safe_name}.png"
        )
        plt.close(fig2)
        
        # Plot performance over time
        fig3 = analyzer.plot_performance_over_time(
            results,
            title=f"Forecast Performance Over Time - {period_name}",
            save_path=f"results/performance_over_time_{safe_name}.png"
        )
        plt.close(fig3)
        
        print(f"  Visualizations saved for: {period_name}")
    
    print()
    
    # Step 5: Generate comprehensive report
    print("Step 5: Generating comprehensive report...")
    
    report = analyzer.generate_summary_report(
        all_metrics,
        all_directional,
        save_path='results/analysis_report.txt'
    )
    
    print("\n" + report)
    
    print()
    print("Analysis complete! Results saved to the 'results' directory.")
    print()
    
    # Step 6: Additional analysis - Weekly and Monthly predictions
    print("Step 6: Running additional horizon analysis...")
    
    # Test different horizons
    horizons = {
        '7-day forecast': 7,
        '30-day forecast': 30
    }
    
    horizon_results = {}
    
    for horizon_name, h in horizons.items():
        print(f"\nTesting {horizon_name}...")
        
        try:
            # Use recent data for horizon testing
            recent_start = (max_date - timedelta(days=180)).strftime('%Y-%m-%d')
            
            results = backtester.backtest_period(
                start_date=recent_start,
                end_date=max_date.strftime('%Y-%m-%d'),
                horizon=h,
                window_size=365,
                step_size=h,
                level=[80, 95]
            )
            
            if len(results) > 0:
                metrics = backtester.calculate_metrics(results)
                horizon_results[horizon_name] = metrics
                
                print(f"  MAPE: {metrics['mape']:.2f}%")
                print(f"  Number of predictions: {metrics['num_predictions']}")
                
                # Save results
                results_file = f"results/horizon_{horizon_name.replace(' ', '_').replace('-', '_')}.csv"
                results.to_csv(results_file, index=False)
            else:
                print(f"  No results for this horizon")
                
        except Exception as e:
            print(f"  Error testing horizon: {e}")
            continue
    
    print()
    print("=" * 80)
    print("Analysis complete!")
    print("Check the 'results' directory for detailed outputs.")
    print("=" * 80)


if __name__ == '__main__':
    main()
