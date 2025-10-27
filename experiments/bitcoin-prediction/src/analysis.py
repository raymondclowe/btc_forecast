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
    
    def plot_accuracy_scorecard(
        self,
        metrics_dict: Dict[str, Dict[str, float]],
        directional_metrics: Dict[str, Dict[str, float]],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create an easy-to-understand scorecard visualization.
        
        Parameters
        ----------
        metrics_dict : Dict[str, Dict[str, float]]
            Dictionary of metrics for different periods
        directional_metrics : Dict[str, Dict[str, float]]
            Dictionary of directional accuracy metrics
        save_path : Optional[str]
            Path to save the plot
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Bitcoin Prediction Performance Scorecard', 
                    fontsize=18, fontweight='bold', y=0.98)
        
        # 1. MAPE comparison across periods
        ax1 = axes[0, 0]
        periods = list(metrics_dict.keys())
        mapes = [metrics_dict[p].get('mape', 0) for p in periods]
        
        colors = ['#06A77D' if m < 10 else '#F77F00' if m < 20 else '#D62828' 
                 for m in mapes]
        
        bars1 = ax1.barh(periods, mapes, color=colors, alpha=0.7, edgecolor='black')
        ax1.set_xlabel('MAPE (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Price Prediction Accuracy\n(Lower is Better)', 
                     fontsize=14, fontweight='bold')
        ax1.axvline(x=10, color='green', linestyle='--', alpha=0.5, label='Excellent (<10%)')
        ax1.axvline(x=20, color='orange', linestyle='--', alpha=0.5, label='Good (<20%)')
        ax1.legend(fontsize=9)
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars1, mapes)):
            ax1.text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
        
        # 2. Directional accuracy comparison
        ax2 = axes[0, 1]
        dir_periods = list(directional_metrics.keys())
        accuracies = [directional_metrics[p].get('accuracy', 0) * 100 for p in dir_periods]
        
        colors2 = ['#06A77D' if a > 55 else '#F77F00' if a > 50 else '#D62828' 
                  for a in accuracies]
        
        bars2 = ax2.barh(dir_periods, accuracies, color=colors2, alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Accuracy (%)', fontsize=12, fontweight='bold')
        ax2.set_title('Directional Prediction Accuracy\n(Up/Down Correct)', 
                     fontsize=14, fontweight='bold')
        ax2.axvline(x=50, color='gray', linestyle='--', alpha=0.5, label='Random (50%)')
        ax2.axvline(x=55, color='green', linestyle='--', alpha=0.5, label='Good (>55%)')
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (bar, val) in enumerate(zip(bars2, accuracies)):
            ax2.text(val + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')
        
        # 3. Confidence interval coverage
        ax3 = axes[1, 0]
        
        if any('coverage_80' in metrics_dict[p] for p in periods):
            cov_80 = [metrics_dict[p].get('coverage_80', 0) * 100 for p in periods]
            cov_95 = [metrics_dict[p].get('coverage_95', 0) * 100 for p in periods]
            
            x = np.arange(len(periods))
            width = 0.35
            
            bars3a = ax3.bar(x - width/2, cov_80, width, label='80% Interval', 
                           color='#F18F01', alpha=0.7, edgecolor='black')
            bars3b = ax3.bar(x + width/2, cov_95, width, label='95% Interval', 
                           color='#C73E1D', alpha=0.7, edgecolor='black')
            
            ax3.set_ylabel('Coverage (%)', fontsize=12, fontweight='bold')
            ax3.set_title('Confidence Interval Coverage\n(Should Match Interval Level)', 
                         fontsize=14, fontweight='bold')
            ax3.set_xticks(x)
            ax3.set_xticklabels(periods, rotation=45, ha='right')
            ax3.axhline(y=80, color='orange', linestyle='--', alpha=0.5)
            ax3.axhline(y=95, color='red', linestyle='--', alpha=0.5)
            ax3.legend(fontsize=10)
            ax3.grid(True, alpha=0.3, axis='y')
            
            # Add value labels
            for bars in [bars3a, bars3b]:
                for bar in bars:
                    height = bar.get_height()
                    ax3.text(bar.get_x() + bar.get_width()/2., height,
                           f'{height:.0f}%', ha='center', va='bottom', fontsize=9)
        
        # 4. Overall performance gauge
        ax4 = axes[1, 1]
        ax4.axis('off')
        
        # Calculate overall scores
        avg_mape = np.mean(mapes)
        avg_accuracy = np.mean(accuracies)
        
        # Determine overall rating
        if avg_mape < 10 and avg_accuracy > 55:
            rating = "EXCELLENT ⭐⭐⭐⭐⭐"
            rating_color = '#06A77D'
        elif avg_mape < 15 and avg_accuracy > 52:
            rating = "GOOD ⭐⭐⭐⭐"
            rating_color = '#5EBB7E'
        elif avg_mape < 20 and avg_accuracy > 50:
            rating = "FAIR ⭐⭐⭐"
            rating_color = '#F77F00'
        else:
            rating = "NEEDS IMPROVEMENT ⭐⭐"
            rating_color = '#D62828'
        
        summary_text = "📊 OVERALL PERFORMANCE\n\n"
        summary_text += f"Rating: {rating}\n\n"
        summary_text += f"Average MAPE: {avg_mape:.1f}%\n"
        summary_text += f"Average Directional Accuracy: {avg_accuracy:.1f}%\n\n"
        summary_text += "━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Add recommendations
        summary_text += "💡 KEY INSIGHTS:\n\n"
        
        if avg_accuracy > 55:
            summary_text += "✓ Good directional signals\n"
        else:
            summary_text += "⚠ Directional signals weak\n"
        
        if avg_mape < 10:
            summary_text += "✓ Excellent price accuracy\n"
        elif avg_mape < 20:
            summary_text += "~ Moderate price accuracy\n"
        else:
            summary_text += "⚠ Use confidence intervals\n"
        
        summary_text += "\n━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        summary_text += "Best Use Cases:\n"
        summary_text += "• Short-term forecasts\n"
        summary_text += "• Risk management\n"
        summary_text += "• Trading signals\n"
        
        ax4.text(0.1, 0.95, summary_text, transform=ax4.transAxes,
                fontsize=12, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor=rating_color, 
                         alpha=0.2, edgecolor='black', linewidth=2))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_simple_performance_summary(
        self,
        backtest_results: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create a simple, easy-to-understand performance summary chart.
        
        Parameters
        ----------
        backtest_results : pd.DataFrame
            DataFrame with backtesting results
        save_path : Optional[str]
            Path to save the plot
            
        Returns
        -------
        plt.Figure
            Matplotlib figure
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Main accuracy visualization
        ax_main = fig.add_subplot(gs[0:2, :])
        
        dates = pd.to_datetime(backtest_results['forecast_date'])
        
        # Calculate whether prediction was good (within 5%)
        results = backtest_results.copy()
        results['good_prediction'] = results['abs_pct_error'] < 5
        
        # Create color-coded scatter plot
        colors = ['#06A77D' if good else '#D62828' 
                 for good in results['good_prediction']]
        sizes = [100 if good else 50 for good in results['good_prediction']]
        
        ax_main.scatter(dates, results['actual'], c=colors, s=sizes, 
                       alpha=0.6, edgecolors='black', linewidth=1.5,
                       label='Predictions (Green=Good, Red=Poor)')
        
        # Add trend line
        ax_main.plot(dates, results['actual'], 'k--', alpha=0.3, linewidth=2)
        
        ax_main.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax_main.set_ylabel('Bitcoin Price (USD)', fontsize=12, fontweight='bold')
        ax_main.set_title('Prediction Quality Over Time\n(Green dots = accurate predictions <5% error)', 
                         fontsize=16, fontweight='bold')
        ax_main.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax_main.grid(True, alpha=0.3)
        
        # Bottom panels - Key metrics
        ax1 = fig.add_subplot(gs[2, 0])
        ax2 = fig.add_subplot(gs[2, 1])
        ax3 = fig.add_subplot(gs[2, 2])
        
        # Panel 1: Win rate
        good_preds = results['good_prediction'].sum()
        total_preds = len(results)
        win_rate = (good_preds / total_preds * 100) if total_preds > 0 else 0
        
        ax1.pie([good_preds, total_preds - good_preds], 
               labels=['Accurate\n(<5% error)', 'Inaccurate\n(>5% error)'],
               colors=['#06A77D', '#D62828'], autopct='%1.0f%%',
               startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Prediction Accuracy', fontsize=12, fontweight='bold')
        
        # Panel 2: Average error
        avg_error = results['abs_pct_error'].mean()
        median_error = results['abs_pct_error'].median()
        
        ax2.barh(['Average', 'Median'], [avg_error, median_error], 
                color=['#F77F00', '#F18F01'], alpha=0.7, edgecolor='black')
        ax2.set_xlabel('Error (%)', fontsize=11, fontweight='bold')
        ax2.set_title('Typical Error Range', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='x')
        
        for i, v in enumerate([avg_error, median_error]):
            ax2.text(v + 0.2, i, f'{v:.1f}%', va='center', fontweight='bold')
        
        # Panel 3: Error distribution
        error_bins = [0, 2, 5, 10, float('inf')]
        error_labels = ['<2%\nExcellent', '2-5%\nGood', '5-10%\nFair', '>10%\nPoor']
        error_counts = pd.cut(results['abs_pct_error'], bins=error_bins, 
                             labels=error_labels).value_counts()
        
        ax3.bar(range(len(error_counts)), error_counts.values, 
               color=['#06A77D', '#5EBB7E', '#F77F00', '#D62828'], 
               alpha=0.7, edgecolor='black')
        ax3.set_xticks(range(len(error_counts)))
        ax3.set_xticklabels(error_labels, fontsize=9)
        ax3.set_ylabel('Count', fontsize=11, fontweight='bold')
        ax3.set_title('Error Categories', fontsize=12, fontweight='bold')
        ax3.grid(True, alpha=0.3, axis='y')
        
        for i, v in enumerate(error_counts.values):
            ax3.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
