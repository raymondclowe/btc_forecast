"""
Data loading and preprocessing utilities for Bitcoin price analysis.
"""
import pandas as pd
import numpy as np
from typing import Tuple, Optional


def load_bitcoin_data(url: str = "https://btcgraphs.pages.dev/btcpricehistory.csv") -> pd.DataFrame:
    """
    Load Bitcoin price history data.
    
    Parameters
    ----------
    url : str
        URL to the Bitcoin price history CSV file
        
    Returns
    -------
    pd.DataFrame
        DataFrame with Bitcoin price history
    """
    df = pd.read_csv(url)
    
    # Ensure we have the expected columns
    if 'Date' in df.columns:
        df['ds'] = pd.to_datetime(df['Date'])
    elif 'date' in df.columns:
        df['ds'] = pd.to_datetime(df['date'])
    else:
        # Assume first column is date
        df['ds'] = pd.to_datetime(df.iloc[:, 0])
    
    # Get price column
    if 'Price' in df.columns:
        df['y'] = df['Price']
    elif 'price' in df.columns:
        df['y'] = df['price']
    elif 'Close' in df.columns:
        df['y'] = df['Close']
    elif 'close' in df.columns:
        df['y'] = df['close']
    else:
        # Assume second column is price
        df['y'] = df.iloc[:, 1]
    
    # Select only needed columns
    df = df[['ds', 'y']].copy()
    
    # Remove any NaN values
    df = df.dropna()
    
    # Sort by date
    df = df.sort_values('ds').reset_index(drop=True)
    
    # Remove duplicate dates (keep last value for each date)
    df = df.drop_duplicates(subset=['ds'], keep='last').reset_index(drop=True)
    
    # Add unique_id for compatibility with TimeGPT
    df['unique_id'] = 'BTC'
    
    # Reorder columns
    df = df[['unique_id', 'ds', 'y']]
    
    return df


def add_derived_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add derived features to the DataFrame.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with Bitcoin price data
        
    Returns
    -------
    pd.DataFrame
        DataFrame with additional features
    """
    df = df.copy()
    
    # Add price changes
    df['price_change'] = df['y'].diff()
    df['price_change_pct'] = df['y'].pct_change() * 100
    
    # Add moving averages
    df['ma_7'] = df['y'].rolling(window=7, min_periods=1).mean()
    df['ma_30'] = df['y'].rolling(window=30, min_periods=1).mean()
    df['ma_90'] = df['y'].rolling(window=90, min_periods=1).mean()
    
    # Add volatility (rolling std)
    df['volatility_7'] = df['y'].rolling(window=7, min_periods=1).std()
    df['volatility_30'] = df['y'].rolling(window=30, min_periods=1).std()
    
    return df


def split_train_test(
    df: pd.DataFrame,
    test_size: int = 30,
    end_date: Optional[str] = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into train and test sets.
    
    Parameters
    ----------
    df : pd.DataFrame
        Full DataFrame
    test_size : int
        Number of days to use for testing
    end_date : Optional[str]
        End date for training data (for backtesting)
        
    Returns
    -------
    Tuple[pd.DataFrame, pd.DataFrame]
        Training and testing DataFrames
    """
    if end_date:
        # Filter data up to end_date
        df_filtered = df[df['ds'] <= end_date].copy()
    else:
        df_filtered = df.copy()
    
    # Split into train and test
    train = df_filtered.iloc[:-test_size].copy()
    test = df_filtered.iloc[-test_size:].copy()
    
    return train, test


def create_directional_labels(df: pd.DataFrame, horizon: int = 1) -> pd.DataFrame:
    """
    Create directional labels (up/down) for prediction.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with price data
    horizon : int
        Number of days ahead to predict
        
    Returns
    -------
    pd.DataFrame
        DataFrame with directional labels
    """
    df = df.copy()
    
    # Create future price column
    df['future_price'] = df['y'].shift(-horizon)
    
    # Create directional label
    df['direction'] = (df['future_price'] > df['y']).astype(int)
    df['direction_label'] = df['direction'].map({1: 'up', 0: 'down'})
    
    # Remove rows without future data
    df = df.dropna(subset=['future_price'])
    
    return df
