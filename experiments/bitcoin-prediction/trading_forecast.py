"""
Bitcoin Trading Forecast Tool - Actionable Daily Predictions.

This tool provides clear, actionable trading signals based on Bit
coin price predictions                                           using open-source StatsForecast models. NO API KEY REQUIRED.

Output includes:
- Predicted direction (up/down) with confidence
- Predicted percent change with confidence  
- Probability ranges for informed position sizing
- Clear trading recommendations (go long, go short, stay out)
"""
import os
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src')
)
from data_utils import load_bitcoin_data


def calculate_confidence_score(prediction_interval_width, histori
cal_volatility):                                                     """
    Calculate confidence score based on prediction interval width
.                                                                    
    Narrow intervals = high confidence
    Wide intervals = low confidence
    """
    # Normalize by historical volatility
    normalized_width = prediction_interval_width / historical_vol
atility                                                              
    # Convert to confidence score (0-100)
    # Lower width = higher confidence
    confidence = max(0, min(100, 100 - (normalized_width * 20)))
    
    return confidence


def get_trading_signal(direction_prob, percent_change, confidence
, range_width):                                                      """
    Generate clear trading signal based on prediction metrics.
    
    Returns: dict with signal, position_size, and reasoning
    """
    signal = {
        'action': 'HOLD',
        'position_size': 0,
        'reasoning': []
    }
    
    # Criteria for trading
    min_confidence = 60
    min_direction_prob = 0.60
    
    if confidence < min_confidence:
        signal['reasoning'].append(f"Low confidence ({confidence:
.0f}%")                                                                 signal['action'] = 'HOLD'
        """
        Bitcoin Trading Forecast Tool - Actionable Daily Predictions.

        This tool provides clear, actionable trading signals based on Bitcoin price predictions
        using open-source StatsForecast models. NO API KEY REQUIRED.

        Output includes:
        - Predicted direction (up/down) with confidence
        - Predicted percent change with confidence
        - Probability ranges for informed position sizing
        - Clear trading recommendations (go long, go short, stay out)
        """
        import os
        import sys
        import pandas as pd
        import numpy as np
        from datetime import datetime

        # Add src to path so data_utils can be imported
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

        from data_utils import load_bitcoin_data


        def calculate_confidence_score(prediction_interval_width, historical_volatility):
            """Calculate confidence score based on prediction interval width.

            Narrow intervals => higher confidence.
            """
            if historical_volatility == 0:
                return 0

            normalized_width = prediction_interval_width / historical_volatility
            confidence = max(0, min(100, 100 - (normalized_width * 20)))
            return confidence


        def get_trading_signal(direction_prob, percent_change, confidence, range_width):
            """Generate a trading signal dict from prediction metrics."""
            signal = {
                'action': 'HOLD',
                'position_size': 0,
                'reasoning': []
            }

            min_confidence = 60
            min_direction_prob = 0.60

            if confidence < min_confidence:
                signal['reasoning'].append(f"Low confidence ({confidence:.0f}%)")
                return signal

            if direction_prob < min_direction_prob:
                signal['reasoning'].append(f"Weak directional signal ({direction_prob*100:.0f}%)")
                return signal

            # Position sizing rules
            if confidence >= 80 and range_width < 0.03:
                position_size = 3
            elif confidence >= 70 and range_width < 0.05:
                position_size = 2
            elif confidence >= 60:
                position_size = 1
            else:
                position_size = 0

            action = 'LONG' if percent_change > 0 else 'SHORT'

            signal['action'] = action
            signal['position_size'] = position_size
            signal['reasoning'].append(f"Predicted change: {percent_change:.2f}%")
            signal['reasoning'].append(f"Confidence: {confidence:.0f}%")
            signal['reasoning'].append(f"Range width: {range_width*100:.2f}%")
            signal['reasoning'].append(f"Directional probability: {direction_prob*100:.0f}%")

            return signal


        def format_forecast_output(forecast_df, current_price, historical_vol=0.05):
            """Prints a human readable forecast and trading signals."""
            print("\n" + "=" * 90)
            print("🚀 BITCOIN TRADING FORECAST - ACTIONABLE SIGNALS")
            print("=" * 90)
            print()
            print(f"📊 Current Bitcoin Price: ${current_price:,.2f}")
            print(f"📅 Forecast Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print()

            for idx, row in forecast_df.iterrows():
                date = row['ds']
                predicted_price = float(row['forecast'])
                lower_80 = float(row.get('lo-80', np.nan))
                upper_80 = float(row.get('hi-80', np.nan))

                percent_change = ((predicted_price - current_price) / current_price) * 100
                range_80_width = (upper_80 - lower_80) / current_price if not np.isnan(lower_80) and not np.isnan(upper_80) else np.nan

                confidence = calculate_confidence_score(range_80_width, historical_vol)
                direction_prob = 0.5 + min(0.3, confidence / 200)

                signal = get_trading_signal(direction_prob, percent_change, confidence, range_80_width if not np.isnan(range_80_width) else 1.0)

                print(f"{date.strftime('%a, %b %d')}: Predicted ${predicted_price:,.2f} ({percent_change:+.2f}%)")
                print(f"  Confidence: {confidence:.0f}% | Direction Prob: {direction_prob*100:.0f}%")
                print(f"  Signal: {signal['action']} | Size: {signal['position_size']} | Reason: {'; '.join(signal['reasoning'])}")
                print("-" * 60)


        def generate_summary_table(forecast_df, current_price, historical_vol=0.05):
            """Print a compact summary table of the next days."""
            print("\nSUMMARY TABLE")
            print("Day | Date       | Price     | Change  | Conf | Signal | Size")
            print("----+------------+-----------+---------+------+--------+-----")
            for idx, row in forecast_df.iterrows():
                day = idx + 1
                date = row['ds'].strftime('%b %d')
                predicted_price = float(row['forecast'])
                lower_80 = float(row.get('lo-80', np.nan))
                upper_80 = float(row.get('hi-80', np.nan))

                percent_change = ((predicted_price - current_price) / current_price) * 100
                range_80_width = (upper_80 - lower_80) / current_price if not np.isnan(lower_80) and not np.isnan(upper_80) else np.nan
                confidence = calculate_confidence_score(range_80_width, historical_vol)
                direction_prob = 0.5 + min(0.3, confidence / 200)
                signal = get_trading_signal(direction_prob, percent_change, confidence, range_80_width if not np.isnan(range_80_width) else 1.0)

                print(f"{day:<3} | {date:<10} | ${predicted_price:>8.0f} | {percent_change:+6.2f}% | {confidence:3.0f}% | {signal['action']:<6} | {signal['position_size']}")


        def main():
            print("\n" + "=" * 80)
            print("🔮 BITCOIN TRADING FORECAST GENERATOR")
            print("=" * 80)

            print("Loading Bitcoin price data...")
            df = load_bitcoin_data()
            df['unique_id'] = 'BTC'

            current_price = df['y'].iloc[-1]

            # Initialize StatsForecast ensemble
            from statsforecast import StatsForecast
            from statsforecast.models import AutoARIMA, AutoETS

            models = [AutoARIMA(season_length=7), AutoETS(season_length=7)]
            sf = StatsForecast(models=models, freq='D', n_jobs=1)

            train_data = df[['unique_id', 'ds', 'y']].copy()
            forecast = sf.forecast(df=train_data, h=7, level=[80, 95])

            if forecast is None or len(forecast) == 0:
                print("Could not generate forecast")
                return

            # Ensemble average across model columns
            cols = [c for c in forecast.columns if c not in ('ds', 'unique_id') and '-lo-' not in c and '-hi-' not in c]
            if len(cols) >= 2:
                forecast['forecast'] = forecast[cols].mean(axis=1)
            else:
                forecast['forecast'] = forecast[cols[0]]

            # Average intervals if present
            lo80 = [c for c in forecast.columns if '-lo-80' in c]
            hi80 = [c for c in forecast.columns if '-hi-80' in c]
            lo95 = [c for c in forecast.columns if '-lo-95' in c]
            hi95 = [c for c in forecast.columns if '-hi-95' in c]
            if lo80:
                forecast['lo-80'] = forecast[lo80].mean(axis=1)
            if hi80:
                forecast['hi-80'] = forecast[hi80].mean(axis=1)
            if lo95:
                forecast['lo-95'] = forecast[lo95].mean(axis=1)
            if hi95:
                forecast['hi-95'] = forecast[hi95].mean(axis=1)

            # Display and save
            format_forecast_output(forecast, current_price)
            generate_summary_table(forecast, current_price)

            out = 'trading_forecast.csv'
            forecast.to_csv(out, index=False)
            print(f"Saved forecast to {out}")


        if __name__ == '__main__':
            main()
        signal['reasoning'].append(f"Weak directional signal ({direction_prob*100:.0f}%)")
        signal['action'] = 'HOLD'
        return signal
    
    # Determine position size based on confidence and range
    if confidence >= 80 and range_width < 0.03:  # High confidence, tight range
        position_size = 3  # Large position
    elif confidence >= 70 and range_width < 0.05:  # Good confidence, moderate range
        position_size = 2  # Medium position
    elif confidence >= 60:  # Moderate confidence
        position_size = 1  # Small position
    else:
        position_size = 0
    
    # Determine action
    if percent_change > 0:
        signal['action'] = 'LONG'
        signal['reasoning'].append(f"Predicted up movement: {percent_change:.2f}%")
    else:
        signal['action'] = 'SHORT'
        signal['reasoning'].append(f"Predicted down movement: {percent_change:.2f}%")
    
    signal['position_size'] = position_size
    signal['reasoning'].append(f"Confidence: {confidence:.0f}%, Range width: {range_width*100:.1f}%")
    signal['reasoning'].append(f"Directional probability: {direction_prob*100:.0f}%")
    
    return signal


def format_forecast_output(forecast_df, current_price):
    """Format forecast data for clear, actionable display."""
    
    print("\n" + "=" * 90)
    print("🚀 BITCOIN TRADING FORECAST - ACTIONABLE SIGNALS")
    print("=" * 90)
    print()
    
    print(f"📊 Current Bitcoin Price: ${current_price:,.2f}")
    print(f"📅 Forecast Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print()
    
    print("-" * 90)
    print("📈 NEXT 7 DAYS FORECAST")
    print("-" * 90)
    print()
    
    for idx, row in forecast_df.iterrows():
        day_num = idx + 1
        date = row['ds']
        predicted_price = row['forecast']
        lower_80 = row['lo-80']
        upper_80 = row['hi-80']
        lower_95 = row['lo-95']
        upper_95 = row['hi-95']
        
        # Calculate metrics
        percent_change = ((predicted_price - current_price) / current_price) * 100
        direction = "📈 UP" if percent_change > 0 else "📉 DOWN"
        
        # Range calculations
        range_80_width = (upper_80 - lower_80) / current_price
        range_95_width = (upper_95 - lower_95) / current_price
        
        # Confidence based on range tightness
        confidence = calculate_confidence_score(range_80_width, 0.05)
        
        # Directional probability (simplified from prediction interval)
        # If price is closer to upper bound, higher probability of up move
        if percent_change > 0:
            direction_prob = 0.5 + min(0.3, confidence / 200)
        else:
            direction_prob = 0.5 + min(0.3, confidence / 200)
        
        # Get trading signal
        signal = get_trading_signal(direction_prob, percent_change, confidence, range_80_width)
        
        # Format output
        print(f"Day {day_num} - {date.strftime('%a, %b %d')}:")
        print(f"  Predicted Price: ${predicted_price:,.2f} ({direction} {abs(percent_change):.2f}%)")
        print(f"  Confidence Level: {confidence:.0f}% {'🟢' if confidence >= 70 else '🟡' if confidence >= 60 else '🔴'}")
        print(f"  Direction Probability: {direction_prob*100:.0f}%")
        print()
        
        print(f"  📊 Price Ranges:")
        print(f"     80% Range: ${lower_80:,.2f} - ${upper_80:,.2f} (width: {range_80_width*100:.1f}%)")
        print(f"     95% Range: ${lower_95:,.2f} - ${upper_95:,.2f} (width: {range_95_width*100:.1f}%)")
        print()
        
        # Trading recommendation
        if signal['action'] == 'LONG':
            emoji = '🟢'
            action_text = f"GO LONG"
        elif signal['action'] == 'SHORT':
            emoji = '🔴'
            action_text = f"GO SHORT"
        else:
            emoji = '⚪'
            action_text = "STAY OUT"
        
        position_text = ['No position', 'Small position', 'Medium position', 'Large position'][signal['position_size']]
        
        print(f"  {emoji} TRADING SIGNAL: {action_text} - {position_text}")
        print(f"     Reasoning: {'; '.join(signal['reasoning'])}")
        print()
        print("-" * 90)
        print()
    
    print("\n" + "=" * 90)
    print("📝 INTERPRETATION GUIDE")
    print("=" * 90)
    print()
    print("Confidence Levels:")
    print("  🟢 70-100%: High confidence - consider larger positions")
    print("  🟡 60-70%:  Moderate confidence - smaller positions")
    print("  🔴 <60%:    Low confidence - stay out or minimal position")
    print()
    print("Position Sizing:")
    print("  Large:   High confidence + tight range + strong signal")
    print("  Medium:  Good confidence + moderate range")
    print("  Small:   Moderate confidence or wider range")
    print("  None:    Low confidence or weak signal")
    print()
    print("Range Width:")
    print("  <3%:  Very tight - high certainty")
    print("  3-5%: Moderate - good for trading")
    print("  >5%:  Wide - higher risk, reduce position size")
    print()
    print("=" * 90)


def generate_summary_table(forecast_df, current_price):
    """Generate a summary table for quick scanning."""
    
    print("\n" + "=" * 90)
    print("📋 QUICK SUMMARY TABLE")
    print("=" * 90)
    print()
    print(f"{'Day':<10} {'Date':<12} {'Price':<12} {'Change':<10} {'Conf':<8} {'Signal':<15} {'Size':<10}")
    print("-" * 90)
    
    for idx, row in forecast_df.iterrows():
        day_num = idx + 1
        date = row['ds'].strftime('%b %d')
        predicted_price = row['forecast']
        lower_80 = row['lo-80']
        upper_80 = row['hi-80']
        
        percent_change = ((predicted_price - current_price) / current_price) * 100
        range_width = (upper_80 - lower_80) / current_price
        confidence = calculate_confidence_score(range_width, 0.05)
        
        direction_prob = 0.5 + min(0.3, confidence / 200)
        signal = get_trading_signal(direction_prob, percent_change, confidence, range_width)
        
        direction_arrow = "📈" if percent_change > 0 else "📉"
        conf_emoji = '🟢' if confidence >= 70 else '🟡' if confidence >= 60 else '🔴'
        
        position_text = ['None', 'Small', 'Medium', 'Large'][signal['position_size']]
        
        print(f"Day {day_num:<5} {date:<12} ${predicted_price:>9,.0f} {direction_arrow}{abs(percent_change):>5.1f}% "
              f"{conf_emoji}{confidence:>4.0f}% {signal['action']:<15} {position_text:<10}")
    
    print("=" * 90)
    print()


def main():
    """Main execution for trading forecast."""
    
    print("\n" + "=" * 90)
    print("🔮 BITCOIN TRADING FORECAST GENERATOR")
    print("Using Open Source StatsForecast Models - NO API KEY REQUIRED")
    print("=" * 90)
    print()
    
    # Load data
    print("Loading Bitcoin price data...")
    df = load_bitcoin_data()
    df['unique_id'] = 'BTC'
    
    current_price = df['y'].iloc[-1]
    current_date = df['ds'].iloc[-1]
    
    print(f"✓ Loaded {len(df)} days of price history")
    print(f"✓ Latest price: ${current_price:,.2f} (as of {current_date.date()})")
    print()
    
    # Initialize StatsForecast with ensemble models
    print("Initializing StatsForecast ensemble (AutoARIMA + AutoETS)...")
    from statsforecast import StatsForecast
    from statsforecast.models import AutoARIMA, AutoETS
    
    models = [
        AutoARIMA(season_length=7),  # Weekly seasonality
        AutoETS(season_length=7),
    ]
    
    sf = StatsForecast(
        models=models,
        freq='D',  # Daily frequency
        n_jobs=1
    )
    
    print("✓ Models initialized")
    print()
    
    # Train on all available data
    print("Training models on full dataset...")
    train_data = df[['unique_id', 'ds', 'y']].copy()
    
    # Generate 7-day forecast
    print("Generating 7-day forecast with confidence intervals...")
    forecast = sf.forecast(df=train_data, h=7, level=[80, 95])
    
    if forecast is None or len(forecast) == 0:
        print("❌ Error: Could not generate forecast")
        return
    
    # Calculate ensemble forecast (average of AutoARIMA and AutoETS)
    forecast_df = forecast.copy()
    model_cols = [col for col in forecast.columns 
                 if col not in ['ds', 'unique_id'] 
                 and '-lo-' not in col and '-hi-' not in col]
    
    if len(model_cols) >= 2:
        # Ensemble: average the models
        forecast_df['forecast'] = forecast[model_cols].mean(axis=1)
    else:
        # Single model
        forecast_df['forecast'] = forecast[model_cols[0]]
    
    # Get confidence intervals (average from both models if available)
    # For simplicity, use first model's intervals (they should be similar)
    lo_80_cols = [col for col in forecast.columns if '-lo-80' in col]
    hi_80_cols = [col for col in forecast.columns if '-hi-80' in col]
    lo_95_cols = [col for col in forecast.columns if '-lo-95' in col]
    hi_95_cols = [col for col in forecast.columns if '-hi-95' in col]
    
    if lo_80_cols:
        forecast_df['lo-80'] = forecast[lo_80_cols].mean(axis=1)
    if hi_80_cols:
        forecast_df['hi-80'] = forecast[hi_80_cols].mean(axis=1)
    if lo_95_cols:
        forecast_df['lo-95'] = forecast[lo_95_cols].mean(axis=1)
    if hi_95_cols:
        forecast_df['hi-95'] = forecast[hi_95_cols].mean(axis=1)
    
    print("✓ Forecast generated successfully")
    print()
    
    # Display results
    format_forecast_output(forecast_df, current_price)
    generate_summary_table(forecast_df, current_price)
    
    # Save forecast to file
    output_file = 'trading_forecast.csv'
    forecast_df.to_csv(output_file, index=False)
    print(f"\n💾 Forecast saved to: {output_file}")
    print()
    
    print("=" * 90)
    print("✅ FORECAST COMPLETE - Use the signals above to inform your trading decisions")
    print("=" * 90)
    print()


if __name__ == '__main__':
    main()
