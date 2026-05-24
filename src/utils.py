import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
import os

def load_config(config_path='config/config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def create_dir_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def print_df_info(df, name="DataFrame"):
    print("\n" + "="*60)
    print(f"{name.upper()} INFO")
    print("="*60)
    print(f"Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nData Types:\n{df.dtypes}")
    print(f"\nMissing Values:\n{df.isnull().sum()}")
    print(f"\nMemory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print("="*60 + "\n")

def plot_missing_values(df, figsize=(10, 6), save_path=None):
    plt.figure(figsize=figsize)
    sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis')
    plt.title('Missing Values Heatmap', fontsize=14, fontweight='bold')
    plt.xlabel('Columns')
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to {save_path}")
    
    plt.tight_layout()
    plt.show()

def save_df_to_csv(df, filepath, name="Data"):
    """Save DataFrame to CSV with confirmation"""
    df.to_csv(filepath, index=False)
    print(f"Saved {name}: {filepath} ({len(df):,} rows)")

def get_timestamp():
    """Get current timestamp string"""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def print_section_header(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

if __name__ == "__main__":
    config = load_config()
    print("Config loaded successfully")
    print(config)