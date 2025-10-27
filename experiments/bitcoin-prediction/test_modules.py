"""
Test script for Bitcoin prediction analysis modules.

This script tests the data loading and processing functions without requiring an API key.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_utils import load_bitcoin_data, add_derived_features, split_train_test, create_directional_labels
import pandas as pd


def test_data_loading():
    """Test data loading functionality."""
    print("Testing data loading...")
    
    try:
        df = load_bitcoin_data()
        
        # Validate structure
        assert 'unique_id' in df.columns, "Missing unique_id column"
        assert 'ds' in df.columns, "Missing ds column"
        assert 'y' in df.columns, "Missing y column"
        assert len(df) > 0, "Empty dataframe"
        assert df['y'].notna().all(), "NaN values in price column"
        
        print(f"  ✓ Loaded {len(df)} days of data")
        print(f"  ✓ Date range: {df['ds'].min()} to {df['ds'].max()}")
        print(f"  ✓ Price range: ${df['y'].min():.2f} to ${df['y'].max():.2f}")
        
        return df
    except Exception as e:
        print(f"  ✗ Error loading data: {e}")
        return None


def test_derived_features(df):
    """Test derived features functionality."""
    print("\nTesting derived features...")
    
    try:
        df_features = add_derived_features(df)
        
        # Validate new columns
        expected_cols = ['price_change', 'price_change_pct', 'ma_7', 'ma_30', 'ma_90', 
                        'volatility_7', 'volatility_30']
        
        for col in expected_cols:
            assert col in df_features.columns, f"Missing column: {col}"
        
        print(f"  ✓ Added {len(expected_cols)} derived features")
        print(f"  ✓ Features: {', '.join(expected_cols)}")
        
        return df_features
    except Exception as e:
        print(f"  ✗ Error adding features: {e}")
        return None


def test_train_test_split(df):
    """Test train/test split functionality."""
    print("\nTesting train/test split...")
    
    try:
        train, test = split_train_test(df, test_size=30)
        
        assert len(train) > 0, "Empty training set"
        assert len(test) == 30, "Test set has wrong size"
        assert train['ds'].max() < test['ds'].min(), "Train and test overlap"
        
        print(f"  ✓ Train size: {len(train)} days")
        print(f"  ✓ Test size: {len(test)} days")
        print(f"  ✓ Train period: {train['ds'].min()} to {train['ds'].max()}")
        print(f"  ✓ Test period: {test['ds'].min()} to {test['ds'].max()}")
        
        return train, test
    except Exception as e:
        print(f"  ✗ Error splitting data: {e}")
        return None, None


def test_directional_labels(df):
    """Test directional label creation."""
    print("\nTesting directional labels...")
    
    try:
        df_dir = create_directional_labels(df, horizon=1)
        
        assert 'direction' in df_dir.columns, "Missing direction column"
        assert 'direction_label' in df_dir.columns, "Missing direction_label column"
        assert df_dir['direction'].isin([0, 1]).all(), "Invalid direction values"
        
        up_count = (df_dir['direction'] == 1).sum()
        down_count = (df_dir['direction'] == 0).sum()
        
        print(f"  ✓ Created directional labels for {len(df_dir)} days")
        print(f"  ✓ Up days: {up_count} ({up_count/len(df_dir)*100:.1f}%)")
        print(f"  ✓ Down days: {down_count} ({down_count/len(df_dir)*100:.1f}%)")
        
        return df_dir
    except Exception as e:
        print(f"  ✗ Error creating labels: {e}")
        return None


def test_data_integrity(df):
    """Test data integrity."""
    print("\nTesting data integrity...")
    
    try:
        # Check for missing values
        missing = df.isnull().sum()
        assert missing.sum() == 0, f"Found missing values: {missing[missing > 0]}"
        
        # Check for duplicates
        duplicates = df.duplicated(subset=['ds']).sum()
        assert duplicates == 0, f"Found {duplicates} duplicate dates"
        
        # Check sorting
        assert df['ds'].is_monotonic_increasing, "Data not sorted by date"
        
        # Check price values
        assert (df['y'] > 0).all(), "Found non-positive prices"
        
        print("  ✓ No missing values")
        print("  ✓ No duplicate dates")
        print("  ✓ Data sorted by date")
        print("  ✓ All prices positive")
        
        return True
    except AssertionError as e:
        print(f"  ✗ Data integrity issue: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 80)
    print("Bitcoin Prediction Analysis - Module Tests")
    print("=" * 80)
    print()
    
    # Test data loading
    df = test_data_loading()
    if df is None:
        print("\n✗ Data loading failed. Aborting tests.")
        return
    
    # Test data integrity
    if not test_data_integrity(df):
        print("\n✗ Data integrity check failed. Aborting tests.")
        return
    
    # Test derived features
    df_features = test_derived_features(df)
    
    # Test train/test split
    train, test = test_train_test_split(df)
    
    # Test directional labels
    df_dir = test_directional_labels(df)
    
    print()
    print("=" * 80)
    print("All tests completed!")
    print("=" * 80)
    print()
    print("To run the full analysis with TimeGPT:")
    print("1. Set your API key: export NIXTLA_API_KEY='your-key-here'")
    print("2. Run: python main.py")
    print()


if __name__ == '__main__':
    main()
