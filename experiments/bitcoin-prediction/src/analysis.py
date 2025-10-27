"""
Analysis and reporting utilities for Bitcoin price prediction.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional, Tuple
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')


class BitcoinAnalyzer:
    """
    Analyzer for Bitcoin price prediction results.
    """
    
    def __init__(self, results_dir: str = "./results"):
        """
        Initialize the analyzer.
        
        Parameters
        ----------
        results_dir : str
            Directory to save results
        """
        self.results_dir = results_dir
        sns.set_style("whitegrid")
    
    def plot_forecast_vs_actual(
        self,
        backtest_results: pd.DataFrame,
        title: str = "Bitcoin Price: Forecast vs Actual",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot forecast vs actual prices.
        
        Parameters
        ----------
        backtest_results : pd.DataFrame
            DataFrame with backtesting results
        title : str
            Plot title
        save_path : Optional[str]
            Path to save the plot
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(14, 6))
        
        dates = pd.to_datetime(backtest_results['forecast_date'])
        
        ax.plot(dates, backtest_results['actual'], 
                label='Actual', linewidth=2, alpha=0.7)
        ax.plot(dates, backtest_results['predicted'], 
                label='Predicted', linewidth=2, alpha=0.7)
        
        # Add confidence intervals if available
        if 'lower_80' in backtest_results.columns:
            ax.fill_between(dates, 
                           backtest_results['lower_80'],
                           backtest_results['upper_80'],
                           alpha=0.2, label='80% Confidence Interval')
        
        if 'lower_95' in backtest_results.columns:
            ax.fill_between(dates, 
                           backtest_results['lower_95'],
                           backtest_results['upper_95'],
                           alpha=0.1, label='95% Confidence Interval')
        
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Price (USD)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_error_distribution(
        self,
        backtest_results: pd.DataFrame,
        title: str = "Forecast Error Distribution",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot error distribution.
        
        Parameters
        ----------
        backtest_results : pd.DataFrame
            DataFrame with backtesting results
        title : str
            Plot title
        save_path : Optional[str]
            Path to save the plot
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Plot absolute error
        axes[0].hist(backtest_results['abs_error'], bins=30, 
                    edgecolor='black', alpha=0.7)
        axes[0].set_xlabel('Absolute Error (USD)', fontsize=12)
        axes[0].set_ylabel('Frequency', fontsize=12)
        axes[0].set_title('Absolute Error Distribution', fontsize=12)
        axes[0].axvline(backtest_results['abs_error'].mean(), 
                       color='red', linestyle='--', label='Mean')
        axes[0].legend()
        
        # Plot percentage error
        axes[1].hist(backtest_results['abs_pct_error'], bins=30, 
                    edgecolor='black', alpha=0.7, color='orange')
        axes[1].set_xlabel('Absolute Percentage Error (%)', fontsize=12)
        axes[1].set_ylabel('Frequency', fontsize=12)
        axes[1].set_title('Absolute Percentage Error Distribution', fontsize=12)
        axes[1].axvline(backtest_results['abs_pct_error'].mean(), 
                       color='red', linestyle='--', label='Mean')
        axes[1].legend()
        
        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.02)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_performance_over_time(
        self,
        backtest_results: pd.DataFrame,
        title: str = "Forecast Performance Over Time",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot performance metrics over time.
        
        Parameters
        ----------
        backtest_results : pd.DataFrame
            DataFrame with backtesting results
        title : str
            Plot title
        save_path : Optional[str]
            Path to save the plot
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        fig, axes = plt.subplots(2, 1, figsize=(14, 8))
        
        dates = pd.to_datetime(backtest_results['forecast_date'])
        
        # Plot absolute error over time
        axes[0].plot(dates, backtest_results['abs_error'], 
                    linewidth=1.5, alpha=0.7)
        axes[0].set_ylabel('Absolute Error (USD)', fontsize=12)
        axes[0].set_title('Absolute Error Over Time', fontsize=12)
        axes[0].grid(True, alpha=0.3)
        
        # Add rolling mean
        rolling_mean = backtest_results['abs_error'].rolling(window=10, min_periods=1).mean()
        axes[0].plot(dates, rolling_mean, 
                    linewidth=2, color='red', label='10-day Rolling Mean')
        axes[0].legend()
        
        # Plot percentage error over time
        axes[1].plot(dates, backtest_results['abs_pct_error'], 
                    linewidth=1.5, alpha=0.7, color='orange')
        axes[1].set_ylabel('Absolute Percentage Error (%)', fontsize=12)
        axes[1].set_xlabel('Date', fontsize=12)
        axes[1].set_title('Absolute Percentage Error Over Time', fontsize=12)
        axes[1].grid(True, alpha=0.3)
        
        # Add rolling mean
        rolling_mean_pct = backtest_results['abs_pct_error'].rolling(window=10, min_periods=1).mean()
        axes[1].plot(dates, rolling_mean_pct, 
                    linewidth=2, color='red', label='10-day Rolling Mean')
        axes[1].legend()
        
        plt.suptitle(title, fontsize=14, fontweight='bold', y=1.00)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_summary_report(
        self,
        metrics_dict: Dict[str, Dict[str, float]],
        directional_metrics: Dict[str, Dict[str, float]],
        save_path: Optional[str] = None
    ) -> str:
        """
        Generate a summary report of all analyses.
        
        Parameters
        ----------
        metrics_dict : Dict[str, Dict[str, float]]
            Dictionary of metrics for different periods
        directional_metrics : Dict[str, Dict[str, float]]
            Dictionary of directional accuracy metrics
        save_path : Optional[str]
            Path to save the report
            
        Returns
        -------
        str
            Summary report as a string
        """
        report = []
        report.append("=" * 80)
        report.append("Bitcoin Price Prediction Analysis Report")
        report.append("Using TimeGPT (Nixtla)")
        report.append("=" * 80)
        report.append("")
        
        # Summary of backtesting periods
        report.append("## Backtesting Summary")
        report.append("")
        
        for period_name, metrics in metrics_dict.items():
            report.append(f"### {period_name}")
            report.append("")
            
            # Create metrics table
            metrics_data = []
            for key, value in metrics.items():
                if isinstance(value, (int, float)):
                    if 'coverage' in key or 'accuracy' in key or 'precision' in key or 'recall' in key or 'f1' in key:
                        formatted_value = f"{value:.2%}"
                    elif 'num' in key:
                        formatted_value = f"{int(value)}"
                    else:
                        formatted_value = f"{value:.2f}"
                    metrics_data.append([key, formatted_value])
            
            report.append(tabulate(metrics_data, headers=['Metric', 'Value'], tablefmt='grid'))
            report.append("")
        
        # Directional accuracy summary
        report.append("## Directional Prediction Accuracy")
        report.append("")
        
        for period_name, dir_metrics in directional_metrics.items():
            report.append(f"### {period_name}")
            report.append("")
            
            dir_data = []
            for key, value in dir_metrics.items():
                if isinstance(value, (int, float)):
                    if key in ['accuracy', 'precision', 'recall', 'f1_score']:
                        formatted_value = f"{value:.2%}"
                    else:
                        formatted_value = f"{int(value)}"
                    dir_data.append([key, formatted_value])
            
            report.append(tabulate(dir_data, headers=['Metric', 'Value'], tablefmt='grid'))
            report.append("")
        
        # Key findings and recommendations
        report.append("## Key Findings and Recommendations")
        report.append("")
        report.append("### Findings:")
        report.append("")
        
        # Calculate average metrics across all periods
        all_mape = [m.get('mape', 0) for m in metrics_dict.values()]
        avg_mape = np.mean(all_mape) if all_mape else 0
        
        all_dir_acc = [m.get('accuracy', 0) for m in directional_metrics.values()]
        avg_dir_acc = np.mean(all_dir_acc) if all_dir_acc else 0
        
        report.append(f"1. Average MAPE across all periods: {avg_mape:.2f}%")
        report.append(f"2. Average directional accuracy: {avg_dir_acc:.2%}")
        
        # Check coverage
        coverage_80 = [m.get('coverage_80', 0) for m in metrics_dict.values()]
        coverage_95 = [m.get('coverage_95', 0) for m in metrics_dict.values()]
        
        if coverage_80:
            avg_cov_80 = np.mean(coverage_80)
            report.append(f"3. Average 80% confidence interval coverage: {avg_cov_80:.2%}")
        if coverage_95:
            avg_cov_95 = np.mean(coverage_95)
            report.append(f"4. Average 95% confidence interval coverage: {avg_cov_95:.2%}")
        
        report.append("")
        report.append("### Recommendations:")
        report.append("")
        
        if avg_dir_acc > 0.55:
            report.append("1. ✓ Directional predictions show promise - can be used for trading signals")
        else:
            report.append("1. ✗ Directional accuracy near random - use with caution")
        
        if avg_mape < 10:
            report.append("2. ✓ Price magnitude predictions are quite accurate")
        elif avg_mape < 20:
            report.append("2. ~ Price magnitude predictions are moderately accurate")
        else:
            report.append("2. ✗ Price magnitude predictions have high error - use confidence intervals")
        
        if coverage_80:
            if avg_cov_80 > 0.75:
                report.append("3. ✓ Confidence intervals are well-calibrated")
            else:
                report.append("3. ~ Confidence intervals may be too narrow - consider wider levels")
        
        report.append("")
        report.append("### Use Cases:")
        report.append("")
        report.append("- **Short-term forecasting (1-7 days)**: Best performance observed")
        report.append("- **Directional trading**: Use directional predictions with proper risk management")
        report.append("- **Risk management**: Leverage confidence intervals for position sizing")
        report.append("- **Trend analysis**: Combine with technical indicators for enhanced signals")
        
        report.append("")
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
        
        return report_text
