"""
Backtesting framework for Bitcoin price prediction.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from nixtla import NixtlaClient
from datetime import timedelta


class BitcoinBacktester:
    """
    Backtesting framework for Bitcoin price predictions.
    """
    
    def __init__(self, client: NixtlaClient, df: pd.DataFrame):
        """
        Initialize the backtester.
        
        Parameters
        ----------
        client : NixtlaClient
            Initialized Nixtla client
        df : pd.DataFrame
            Full Bitcoin price history
        """
        self.client = client
        self.df = df
        
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
            Confidence levels for prediction intervals
            
        Returns
        -------
        pd.DataFrame
            DataFrame with backtesting results
        """
        # Filter data for the backtesting period
        df_period = self.df[
            (self.df['ds'] >= start_date) & 
            (self.df['ds'] <= end_date)
        ].copy()
        
        results = []
        
        # Get unique dates
        dates = df_period['ds'].unique()
        
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
                # Make forecast
                forecast = self.client.forecast(
                    df=train_data,
                    h=horizon,
                    level=level
                )
                
                predicted_value = forecast['TimeGPT'].values[-1]
                
                result = {
                    'train_start': train_start_date,
                    'train_end': train_end_date,
                    'forecast_date': actual_date,
                    'actual': actual_value,
                    'predicted': predicted_value,
                    'error': actual_value - predicted_value,
                    'abs_error': abs(actual_value - predicted_value),
                    'pct_error': ((actual_value - predicted_value) / actual_value) * 100,
                    'abs_pct_error': abs((actual_value - predicted_value) / actual_value) * 100
                }
                
                # Add confidence intervals if provided
                if level:
                    for lv in level:
                        result[f'lower_{lv}'] = forecast[f'TimeGPT-lo-{lv}'].values[-1]
                        result[f'upper_{lv}'] = forecast[f'TimeGPT-hi-{lv}'].values[-1]
                        result[f'in_interval_{lv}'] = (
                            actual_value >= forecast[f'TimeGPT-lo-{lv}'].values[-1]
                        ) and (
                            actual_value <= forecast[f'TimeGPT-hi-{lv}'].values[-1]
                        )
                
                results.append(result)
                
            except Exception as e:
                print(f"Error forecasting for {test_date}: {e}")
                continue
        
        return pd.DataFrame(results)
    
    def evaluate_directional_accuracy(self, backtest_results: pd.DataFrame) -> Dict[str, float]:
        """
        Evaluate directional prediction accuracy.
        
        Parameters
        ----------
        backtest_results : pd.DataFrame
            DataFrame with backtesting results
            
        Returns
        -------
        Dict[str, float]
            Dictionary with directional accuracy metrics
        """
        # Calculate actual direction
        results = backtest_results.copy()
        
        # Get previous actual value for each prediction
        results['prev_actual'] = results['actual'].shift(1)
        results = results.dropna(subset=['prev_actual'])
        
        results['actual_direction'] = (results['actual'] > results['prev_actual']).astype(int)
        results['predicted_direction'] = (results['predicted'] > results['prev_actual']).astype(int)
        
        # Calculate accuracy
        correct = (results['actual_direction'] == results['predicted_direction']).sum()
        total = len(results)
        accuracy = correct / total if total > 0 else 0
        
        # Calculate precision and recall for "up" direction
        tp = ((results['actual_direction'] == 1) & (results['predicted_direction'] == 1)).sum()
        fp = ((results['actual_direction'] == 0) & (results['predicted_direction'] == 1)).sum()
        fn = ((results['actual_direction'] == 1) & (results['predicted_direction'] == 0)).sum()
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'total_predictions': total,
            'correct_predictions': correct
        }
    
    def calculate_metrics(self, backtest_results: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate comprehensive metrics from backtesting results.
        
        Parameters
        ----------
        backtest_results : pd.DataFrame
            DataFrame with backtesting results
            
        Returns
        -------
        Dict[str, float]
            Dictionary with various metrics
        """
        metrics = {
            'mae': backtest_results['abs_error'].mean(),
            'rmse': np.sqrt((backtest_results['error'] ** 2).mean()),
            'mape': backtest_results['abs_pct_error'].mean(),
            'median_ape': backtest_results['abs_pct_error'].median(),
            'std_error': backtest_results['error'].std(),
            'mean_error': backtest_results['error'].mean(),
            'num_predictions': len(backtest_results)
        }
        
        # Add coverage metrics if confidence intervals exist
        for col in backtest_results.columns:
            if col.startswith('in_interval_'):
                level = col.split('_')[-1]
                coverage = backtest_results[col].mean()
                metrics[f'coverage_{level}'] = coverage
        
        return metrics
