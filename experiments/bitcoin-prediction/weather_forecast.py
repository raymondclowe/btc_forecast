"""
Bitcoin Weather Forecast Tool

A simple, intuitive tool that provides a "weather forecast" style outlook
for Bitcoin prices over the next few days, showing ranges and probabilities.
"""
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime, timedelta
from nixtla import NixtlaClient
from dotenv import load_dotenv

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_utils import load_bitcoin_data


def create_weather_forecast_chart(
    df: pd.DataFrame,
    forecast_df: pd.DataFrame,
    save_path: str = None
) -> plt.Figure:
    """
    Create an easy-to-understand weather forecast style chart for Bitcoin.
    
    Parameters
    ----------
    df : pd.DataFrame
        Historical data
    forecast_df : pd.DataFrame
        Forecast data with confidence intervals
    save_path : str, optional
        Path to save the chart
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    # Use a clean, modern style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    fig = plt.figure(figsize=(16, 10))
    
    # Create grid for subplots
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3, height_ratios=[2, 1, 1])
    
    # Main forecast chart
    ax_main = fig.add_subplot(gs[0, :])
    
    # Get last 30 days of historical data
    recent_df = df.tail(30).copy()
    current_price = recent_df['y'].iloc[-1]
    current_date = recent_df['ds'].iloc[-1]
    
    # Plot historical prices
    ax_main.plot(recent_df['ds'], recent_df['y'], 
                linewidth=3, color='#2E86AB', label='Historical Price', 
                marker='o', markersize=4, alpha=0.8)
    
    # Plot forecast
    forecast_dates = pd.to_datetime(forecast_df['ds'])
    forecast_prices = forecast_df['TimeGPT']
    
    ax_main.plot(forecast_dates, forecast_prices, 
                linewidth=3, color='#A23B72', label='Forecast', 
                marker='s', markersize=6, linestyle='--', alpha=0.9)
    
    # Add confidence intervals with gradient effect
    if 'TimeGPT-lo-95' in forecast_df.columns:
        ax_main.fill_between(
            forecast_dates,
            forecast_df['TimeGPT-lo-95'],
            forecast_df['TimeGPT-hi-95'],
            alpha=0.15, color='#F18F01', label='95% Confidence Range'
        )
    
    if 'TimeGPT-lo-80' in forecast_df.columns:
        ax_main.fill_between(
            forecast_dates,
            forecast_df['TimeGPT-lo-80'],
            forecast_df['TimeGPT-hi-80'],
            alpha=0.25, color='#C73E1D', label='80% Confidence Range'
        )
    
    # Add vertical line at current date
    ax_main.axvline(x=current_date, color='gray', linestyle=':', linewidth=2, alpha=0.5)
    ax_main.text(current_date, ax_main.get_ylim()[1] * 0.95, 'TODAY', 
                ha='center', fontsize=12, fontweight='bold', color='gray')
    
    # Formatting
    ax_main.set_xlabel('Date', fontsize=14, fontweight='bold')
    ax_main.set_ylabel('Bitcoin Price (USD)', fontsize=14, fontweight='bold')
    ax_main.set_title('Bitcoin Price Forecast - Next 7 Days', 
                     fontsize=18, fontweight='bold', pad=20)
    ax_main.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax_main.grid(True, alpha=0.3, linestyle='--')
    ax_main.tick_params(labelsize=11)
    
    # Format y-axis as currency
    ax_main.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Daily outlook panel
    ax_daily = fig.add_subplot(gs[1, :])
    ax_daily.axis('off')
    
    # Create daily outlook
    daily_text = "📅 DAILY OUTLOOK:\n\n"
    
    for i in range(min(7, len(forecast_df))):
        date = forecast_dates.iloc[i].strftime('%a, %b %d')
        price = forecast_prices.iloc[i]
        
        if i == 0:
            change_from = current_price
        else:
            change_from = forecast_prices.iloc[i-1]
        
        change_pct = ((price - change_from) / change_from) * 100
        
        # Determine trend emoji
        if change_pct > 2:
            trend = "📈 Strong Up"
            color = '#06A77D'
        elif change_pct > 0.5:
            trend = "↗️  Up"
            color = '#5EBB7E'
        elif change_pct < -2:
            trend = "📉 Strong Down"
            color = '#D62828'
        elif change_pct < -0.5:
            trend = "↘️  Down"
            color = '#F77F00'
        else:
            trend = "➡️  Flat"
            color = '#6C757D'
        
        # Get confidence range if available
        if 'TimeGPT-lo-80' in forecast_df.columns:
            lo_80 = forecast_df['TimeGPT-lo-80'].iloc[i]
            hi_80 = forecast_df['TimeGPT-hi-80'].iloc[i]
            range_text = f"${lo_80:,.0f} - ${hi_80:,.0f}"
        else:
            range_text = "N/A"
        
        daily_text += f"{date}: ${price:,.0f} {trend} (Range: {range_text})\n"
    
    ax_daily.text(0.05, 0.95, daily_text, transform=ax_daily.transAxes,
                 fontsize=11, verticalalignment='top', family='monospace',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # Probability/Confidence panel
    ax_prob = fig.add_subplot(gs[2, 0])
    ax_prob.axis('off')
    
    # Calculate directional probabilities (simplified)
    up_days = (forecast_prices.diff().dropna() > 0).sum()
    total_days = len(forecast_prices) - 1
    up_prob = (up_days / total_days * 100) if total_days > 0 else 50
    down_prob = 100 - up_prob
    
    prob_text = "📊 DIRECTIONAL OUTLOOK:\n\n"
    prob_text += f"↗️  Upward Movement: {up_prob:.0f}%\n"
    prob_text += f"↘️  Downward Movement: {down_prob:.0f}%\n\n"
    
    # Overall trend
    final_price = forecast_prices.iloc[-1]
    total_change = ((final_price - current_price) / current_price) * 100
    
    if total_change > 0:
        prob_text += f"Week Outlook: +{total_change:.1f}% 📈"
    else:
        prob_text += f"Week Outlook: {total_change:.1f}% 📉"
    
    ax_prob.text(0.05, 0.95, prob_text, transform=ax_prob.transAxes,
                fontsize=11, verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    # Volatility/Uncertainty panel
    ax_uncert = fig.add_subplot(gs[2, 1])
    ax_uncert.axis('off')
    
    uncert_text = "⚠️  UNCERTAINTY LEVEL:\n\n"
    
    # Calculate average range width as proxy for uncertainty
    if 'TimeGPT-lo-80' in forecast_df.columns:
        avg_range = (forecast_df['TimeGPT-hi-80'] - forecast_df['TimeGPT-lo-80']).mean()
        range_pct = (avg_range / forecast_prices.mean()) * 100
        
        if range_pct < 5:
            uncert_level = "Low 🟢"
        elif range_pct < 10:
            uncert_level = "Moderate 🟡"
        else:
            uncert_level = "High 🔴"
        
        uncert_text += f"Uncertainty: {uncert_level}\n"
        uncert_text += f"Avg Range: ±${avg_range/2:,.0f}\n"
        uncert_text += f"Range %: ±{range_pct/2:.1f}%\n\n"
    
    uncert_text += "💡 Tip: Wider ranges indicate\n"
    uncert_text += "   higher uncertainty."
    
    ax_uncert.text(0.05, 0.95, uncert_text, transform=ax_uncert.transAxes,
                  fontsize=11, verticalalignment='top', family='monospace',
                  bbox=dict(boxstyle='round', facecolor='#FFE5B4', alpha=0.3))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Weather forecast chart saved to: {save_path}")
    
    return fig


def create_simple_outlook_chart(
    current_price: float,
    forecast_df: pd.DataFrame,
    save_path: str = None
) -> plt.Figure:
    """
    Create a simple, colorful outlook chart showing probability ranges.
    
    Parameters
    ----------
    current_price : float
        Current Bitcoin price
    forecast_df : pd.DataFrame
        Forecast data
    save_path : str, optional
        Path to save the chart
        
    Returns
    -------
    plt.Figure
        The figure object
    """
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left chart: Bar chart of daily forecasts with error bars
    ax1 = axes[0]
    
    dates = pd.to_datetime(forecast_df['ds'])
    prices = forecast_df['TimeGPT']
    
    # Calculate error bars
    if 'TimeGPT-lo-80' in forecast_df.columns:
        lower_err = prices - forecast_df['TimeGPT-lo-80']
        upper_err = forecast_df['TimeGPT-hi-80'] - prices
        yerr = [lower_err, upper_err]
    else:
        yerr = None
    
    # Color bars based on change from previous
    colors = []
    for i in range(len(prices)):
        if i == 0:
            change = prices.iloc[i] - current_price
        else:
            change = prices.iloc[i] - prices.iloc[i-1]
        
        if change > 0:
            colors.append('#06A77D')  # Green for up
        else:
            colors.append('#D62828')  # Red for down
    
    x_labels = [d.strftime('%a\n%m/%d') for d in dates]
    x_pos = range(len(x_labels))
    
    bars = ax1.bar(x_pos, prices, color=colors, alpha=0.7, 
                   edgecolor='black', linewidth=1.5)
    
    if yerr:
        ax1.errorbar(x_pos, prices, yerr=yerr, fmt='none', 
                    ecolor='black', capsize=5, capthick=2, alpha=0.5)
    
    # Add current price line
    ax1.axhline(y=current_price, color='blue', linestyle='--', 
               linewidth=2, label=f'Current: ${current_price:,.0f}')
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x_labels, fontsize=10)
    ax1.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')
    ax1.set_title('Daily Price Forecast with Confidence Ranges', 
                 fontsize=14, fontweight='bold')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Right chart: Range fan chart
    ax2 = axes[1]
    
    if 'TimeGPT-lo-95' in forecast_df.columns:
        days = range(len(forecast_df))
        
        # Plot median forecast
        ax2.plot(days, prices, 'ko-', linewidth=3, markersize=8, 
                label='Forecast', zorder=5)
        
        # Plot confidence fans
        ax2.fill_between(days, 
                        forecast_df['TimeGPT-lo-95'], 
                        forecast_df['TimeGPT-hi-95'],
                        alpha=0.2, color='red', label='95% Range')
        ax2.fill_between(days, 
                        forecast_df['TimeGPT-lo-80'], 
                        forecast_df['TimeGPT-hi-80'],
                        alpha=0.3, color='orange', label='80% Range')
        
        # Add decreasing certainty annotation
        for i in [0, len(days)//2, len(days)-1]:
            if i < len(days):
                y_pos = prices.iloc[i]
                ax2.annotate(f'Day {i+1}', xy=(i, y_pos), 
                           xytext=(10, 10), textcoords='offset points',
                           fontsize=9, alpha=0.7)
        
        ax2.set_xlabel('Days Ahead', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')
        ax2.set_title('Uncertainty Increases Over Time', 
                     fontsize=14, fontweight='bold')
        ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # Add annotation about uncertainty
        ax2.text(0.5, 0.02, '← More Certain  |  Less Certain →', 
                transform=ax2.transAxes, ha='center', fontsize=10,
                style='italic', alpha=0.7)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Simple outlook chart saved to: {save_path}")
    
    return fig


def main():
    """Main weather forecast tool."""
    
    # Load environment variables
    load_dotenv()
    
    # Initialize client
    api_key = os.environ.get('NIXTLA_API_KEY')
    if not api_key:
        print("❌ Error: NIXTLA_API_KEY not found in environment.")
        print("Set your API key with: export NIXTLA_API_KEY='your-key-here'")
        return
    
    client = NixtlaClient(api_key=api_key)
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    print("=" * 80)
    print("🌤️  BITCOIN WEATHER FORECAST")
    print("=" * 80)
    print()
    
    # Load data
    print("Loading Bitcoin price data...")
    df = load_bitcoin_data()
    
    current_price = df['y'].iloc[-1]
    current_date = df['ds'].iloc[-1]
    
    print(f"✓ Current Bitcoin Price: ${current_price:,.2f}")
    print(f"✓ As of: {current_date.strftime('%Y-%m-%d %H:%M')}")
    print()
    
    # Use last 180 days for training
    train_df = df.tail(180).copy()
    
    print("Generating 7-day forecast with confidence intervals...")
    print("(This may take a moment...)")
    print()
    
    try:
        # Generate forecast
        forecast_df = client.forecast(
            df=train_df,
            h=7,
            level=[80, 95]
        )
        
        print("✓ Forecast generated successfully!")
        print()
        
        # Display forecast summary
        print("📊 FORECAST SUMMARY:")
        print("-" * 80)
        
        for i in range(len(forecast_df)):
            date = pd.to_datetime(forecast_df['ds'].iloc[i])
            price = forecast_df['TimeGPT'].iloc[i]
            
            if i == 0:
                change = price - current_price
            else:
                change = price - forecast_df['TimeGPT'].iloc[i-1]
            
            change_pct = (change / current_price) * 100
            
            # Get confidence range
            if 'TimeGPT-lo-80' in forecast_df.columns:
                lo = forecast_df['TimeGPT-lo-80'].iloc[i]
                hi = forecast_df['TimeGPT-hi-80'].iloc[i]
                range_str = f" (Range: ${lo:,.0f} - ${hi:,.0f})"
            else:
                range_str = ""
            
            trend = "📈" if change > 0 else "📉" if change < 0 else "➡️"
            
            print(f"{date.strftime('%a, %b %d')}: ${price:,.2f} {trend} "
                  f"({change_pct:+.1f}%){range_str}")
        
        print("-" * 80)
        print()
        
        # Calculate week outlook
        final_price = forecast_df['TimeGPT'].iloc[-1]
        week_change = final_price - current_price
        week_change_pct = (week_change / current_price) * 100
        
        print(f"📈 WEEK OUTLOOK: {week_change_pct:+.1f}% "
              f"(${current_price:,.0f} → ${final_price:,.0f})")
        print()
        
        # Create weather forecast chart
        print("Creating weather forecast chart...")
        fig1 = create_weather_forecast_chart(
            df, 
            forecast_df,
            save_path='results/bitcoin_weather_forecast.png'
        )
        plt.close(fig1)
        
        # Create simple outlook chart
        print("Creating simple outlook chart...")
        fig2 = create_simple_outlook_chart(
            current_price,
            forecast_df,
            save_path='results/bitcoin_simple_outlook.png'
        )
        plt.close(fig2)
        
        print()
        print("=" * 80)
        print("✅ Weather forecast complete!")
        print()
        print("📁 Charts saved to:")
        print("   - results/bitcoin_weather_forecast.png")
        print("   - results/bitcoin_simple_outlook.png")
        print()
        print("💡 TIP: Charts show decreasing certainty over time.")
        print("    Use confidence ranges for risk management!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Error generating forecast: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
