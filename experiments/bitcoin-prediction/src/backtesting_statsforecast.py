"""
Backtesting framework for Bitcoin price prediction using open-source StatsForecast.
No API key required - runs locally.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import timedelta
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, AutoETS, SeasonalNaive


class BitcoinBacktester:
    """
    Backtesting framework for Bitcoin price predictions using StatsForecast.
    """
    
    def __init__(self, df: pd.DataFrame, model_type: str = 'auto'):
        """
        Initialize the backtester.
        
        Parameters
        ----------
        df : pd.DataFrame
            Full Bitcoin price history with columns: unique_id, ds, y
        model_type : str
            Model to use: 'auto' (AutoARIMA+AutoETS), 'arima', 'ets', 'ensemble'
        """
        self.df = df
        self.model_type = model_type
        
        # Initialize models based on type
        if model_type == 'auto' or model_type == 'ensemble':
            self.models = [
                AutoARIMA(season_length=7),  # Weekly seasonality
                AutoETS(season_length=7),
            ]
        elif model_type == 'arima':
            self.models = [AutoARIMA(season_length=7)]
        elif model_type == 'ets':
            self.models = [AutoETS(season_length=7)]
        else:
            # Default to AutoARIMA
            self.models = [AutoARIMA(season_length=7)]
        
    def backtest_period(
        self,
        start_date: str,
        end_date: str,
        horizon: int = 1,
        window_size: int = 365,
        step_size: int = 7,
        level: Optional[List[int]] = None
    ) -> pd.DataFrame:
        """
        Perform backtesting over a specified period.
        
        Parameters
        ----------
        start_date : str
            Start date for backtesting
        end_date : str
            End date for backtesting
        horizon : int
            Forecast horizon in days
        window_size : int
            Size of training window in days
        step_size : int
            Number of days to step forward for each iteration
        level : Optional[List[int]]
            Confidence levels for prediction intervals (e.g., [80, 95])
            
        Returns
        -------
        pd.DataFrame
            DataFrame with backtesting results
        """
        if level is None:
            level = [80, 95]
        
        # Filter data for the backtesting period
        df_period = self.df[
            (self.df['ds'] >= start_date) & 
            (self.df['ds'] <= end_date)
        ].copy()
        
        results = []
        
        # Get unique dates
        dates = sorted(df_period['ds'].unique())
        
        # Iterate through dates with step size
        for i in range(0, len(dates) - window_size - horizon, step_size):
            test_date = dates[i + window_size]
            
            # Get training data
            train_end_date = dates[i + window_size - 1]
            train_start_date = dates[i]
            
            train_data = self.df[
                (self.df['ds'] >= train_start_date) &
                (self.df['ds'] <= train_end_date)
            ].copy()
            
            # Get actual value
            actual_idx = i + window_size + horizon - 1
            if actual_idx >= len(dates):
                break
                
            actual_date = dates[actual_idx]
            actual_value = df_period[df_period['ds'] == actual_date]['y'].values
            
            if len(actual_value) == 0:
                continue
                
            actual_value = actual_value[0]
            
            try:
                # Ensure train_data has unique_id column as string
                train_data_sf = train_data.copy()
                if 'unique_id' not in train_data_sf.columns:
                    train_data_sf['unique_id'] = 'BTC'
                
                # Make forecast using StatsForecast
                sf = StatsForecast(
                    models=self.models,
                    freq='D',  # Daily frequency
                    n_jobs=1  # Single job to avoid issues
                )
                
                # Fit and forecast
                forecast_df = sf.forecast(df=train_data_sf[['unique_id', 'ds', 'y']], h=horizon, level=level)
                
                # Get the last forecast (for the horizon)
                forecast_row = forecast_df.iloc[-1]
                
                # Ensemble: average predictions from multiple models if available
                if self.model_type == 'ensemble' or self.model_type == 'auto':
                    # Average the predictions from different models
                    # Columns are like: unique_id, ds, AutoARIMA, AutoARIMA-lo-95, etc.
                    model_cols = [col for col in forecast_df.columns 
                                 if col not in ['ds', 'unique_id'] 
                                 and '-lo-' not in col and '-hi-' not in col]
                    if len(model_cols) > 0:
                        predicted_value = forecast_df[model_cols].iloc[-1].mean()
                    else:
                        predicted_value = forecast_row.iloc[2]  # Third column (after unique_id, ds)
                else:
                    # Single model - get the first prediction column
                    pred_col = [col for col in forecast_df.columns 
                               if col not in ['ds', 'unique_id'] 
                               and '-lo-' not in col and '-hi-' not in col][0]
                    predicted_value = forecast_row[pred_col]
                
                # Extract confidence intervals
                result_dict = {
                    'train_start': train_start_date,
                    'train_end': train_end_date,
                    'forecast_date': actual_date,
                    'actual': actual_value,
                    'predicted': predicted_value,
                    'error': actual_value - predicted_value,
                    'abs_error': abs(actual_value - predicted_value),
                    'pct_error': ((actual_value - predicted_value) / actual_value) * 100,
                    'abs_pct_error': abs((actual_value - predicted_value) / actual_value) * 100,
                }
                
                # Add confidence intervals if available
                for lv in level:
                    # Find columns matching this level
                    lo_cols = [col for col in forecast_df.columns if f'-lo-{lv}' in col]
                    hi_cols = [col for col in forecast_df.columns if f'-hi-{lv}' in col]
                    
                    if lo_cols and hi_cols:
                        # Average across models for ensemble
                        lower = forecast_df[lo_cols].iloc[-1].mean()
                        upper = forecast_df[hi_cols].iloc[-1].mean()
                        
                        result_dict[f'lower_{lv}'] = float(lower)
                        result_dict[f'upper_{lv}'] = float(upper)
                        result_dict[f'in_interval_{lv}'] = lower <= actual_value <= upper
                
                results.append(result_dict)
                
            except Exception as e:
                print(f"Error forecasting for {actual_date}: {e}")
                continue
        
        if len(results) == 0:
            return pd.DataFrame()
        
        return pd.DataFrame(results)
    
    def calculate_metrics(self, results: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate performance metrics from backtesting results.
        
        Parameters
        ----------
        results : pd.DataFrame
            Backtesting results
            
        Returns
        -------
        Dict[str, float]
            Dictionary of metrics
        """
        if len(results) == 0:
            return {}
        
        metrics = {
            'mae': results['abs_error'].mean(),
            'rmse': np.sqrt((results['error'] ** 2).mean()),
            'mape': results['abs_pct_error'].mean(),
            'median_ape': results['abs_pct_error'].median(),
            'std_error': results['error'].std(),
            'mean_error': results['error'].mean(),
            'num_predictions': len(results),
        }
        
        # Coverage metrics for confidence intervals
        for col in results.columns:
            if col.startswith('in_interval_'):
                level = col.split('_')[-1]
                metrics[f'coverage_{level}'] = results[col].mean()
        
        return metrics
    
    def evaluate_directional_accuracy(self, results: pd.DataFrame) -> Dict[str, float]:
        """
        Evaluate directional prediction accuracy.
        
        Parameters
        ----------
        results : pd.DataFrame
            Backtesting results
            
        Returns
        -------
        Dict[str, float]
            Dictionary of directional metrics
        """
        if len(results) == 0:
            return {}
        
        # Calculate actual and predicted directions
        results_copy = results.copy()
        
        # Get previous actual values to determine direction
        results_copy['actual_direction'] = np.where(results_copy['error'] < 0, 1, 0)  # 1 if price went up
        results_copy['predicted_direction'] = 1  # Predict up if prediction > previous
        
        # For a more accurate direction, we need to know if price increased from previous day
        # Since we have train_end, we can compare forecast to that
        # Simplified: if error is negative, we under-predicted (price went up)
        # if error is positive, we over-predicted (price went down)
        
        # Calculate directional predictions
        correct_direction = 0
        true_positives = 0
        false_positives = 0
        true_negatives = 0
        false_negatives = 0
        
        for idx, row in results_copy.iterrows():
            # Actual direction: did price go up?
            actual_up = row['error'] < 0  # Under-predicted means price went up
            
            # Get previous price from train_end
            # For simplicity, assume if predicted > actual, we predicted up
            # This is approximate but works for direction
            
            # Better approach: compare predicted change
            train_end_val = results_copy.loc[idx, 'actual'] - results_copy.loc[idx, 'error']  # Previous value
            actual_direction = row['actual'] > train_end_val
            predicted_direction = row['predicted'] > train_end_val
            
            if actual_direction == predicted_direction:
                correct_direction += 1
                if actual_direction:
                    true_positives += 1
                else:
                    true_negatives += 1
            else:
                if predicted_direction:
                    false_positives += 1
                else:
                    false_negatives += 1
        
        total = len(results_copy)
        accuracy = correct_direction / total if total > 0 else 0
        
        # Calculate precision, recall, F1
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'total_predictions': total,
            'correct_predictions': correct_direction,
        }
