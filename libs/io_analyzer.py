"""
IO Table Analysis Library
Provides filtering and bidirectional analysis functions
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


def load_config(config_path: str = 'config.json') -> Dict:
    """
    Load configuration from JSON file

    Parameters
    ----------
    config_path : str
        Path to config.json file

    Returns
    -------
    dict
        Configuration dictionary
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config


def load_data(config: Dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load transaction and index dataframes from config paths
    
    Parameters
    ----------
    config : dict
        Configuration dictionary
        
    Returns
    -------
    tuple
        (transaction_df, index_df)
    """
    data_config = config['data_source']
    
    df_trans = pd.read_csv(
        data_config['transaction_data_path'],
        encoding='utf-8-sig'
    )
    
    df_index = pd.read_csv(
        data_config['index_data_path'],
        encoding='utf-8-sig'
    )
    
    return df_trans, df_index


def apply_filters(df: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """
    Apply all filters from config to dataframe
    
    Parameters
    ----------
    df : pd.DataFrame
        Transaction dataframe
    config : dict
        Configuration dictionary
        
    Returns
    -------
    pd.DataFrame
        Filtered dataframe
    """
    df_filtered = df.copy()
    filters = config.get('filters', {})
    
    # Filter by geographical level
    if filters.get('geographical_level'):
        df_filtered = df_filtered[
            df_filtered['geographical_level'] == filters['geographical_level']
        ]
    
    # Filter by tables (only if column exists)
    if filters.get('tables') and 'table' in df_filtered.columns:
        df_filtered = df_filtered[
            df_filtered['table'].isin(filters['tables'])
        ]
    
    # Filter by output region (only if column exists)
    if filters.get('output_region') and 'output_region' in df_filtered.columns:
        df_filtered = df_filtered[
            df_filtered['output_region'] == filters['output_region']
        ]

    # Filter by input region (only if column exists)
    if filters.get('input_region') and 'input_region' in df_filtered.columns:
        df_filtered = df_filtered[
            df_filtered['input_region'] == filters['input_region']
        ]
    
    # Filter by output sectors
    if filters.get('output_sectors'):
        df_filtered = df_filtered[
            df_filtered['output_sector_code'].astype(str).isin(
                [str(s) for s in filters['output_sectors']]
            )
        ]
    
    # Filter by input sectors
    if filters.get('input_sectors'):
        df_filtered = df_filtered[
            df_filtered['input_sector_code'].astype(str).isin(
                [str(s) for s in filters['input_sectors']]
            )
        ]
    
    # Filter by value range
    if filters.get('min_value') is not None:
        df_filtered = df_filtered[
            df_filtered['value'] >= filters['min_value']
        ]
    
    if filters.get('max_value') is not None:
        df_filtered = df_filtered[
            df_filtered['value'] <= filters['max_value']
        ]
    
    return df_filtered


def analyze_forward(df: pd.DataFrame, aggregation: str = 'sum') -> pd.DataFrame:
    """
    Forward analysis: Output Sector → Input Sector
    Calculate total input requirements for each output sector
    
    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction dataframe
    aggregation : str
        Aggregation function: 'sum', 'mean', 'median', 'max', 'min'
        
    Returns
    -------
    pd.DataFrame
        Forward analysis results
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Group by output and input sectors
    groupby_cols = ['output_sector_code', 'output_sector_name']
    
    # Check if regional data exists
    if 'output_region' in df.columns and df['output_region'].notna().any():
        groupby_cols.insert(0, 'output_region')
    
    groupby_cols.extend(['input_sector_code', 'input_sector_name'])
    
    if 'input_region' in df.columns and df['input_region'].notna().any():
        groupby_cols.insert(len(groupby_cols)-2, 'input_region')
    
    # Apply aggregation
    result = df.groupby(groupby_cols)['value'].agg(aggregation).reset_index()
    result.columns = groupby_cols + ['value']
    
    # Sort by output sector and value (descending)
    sort_cols = [col for col in groupby_cols if 'region' not in col][:2]
    result = result.sort_values(sort_cols + ['value'], ascending=[True, True, False])
    
    return result


def analyze_backward(df: pd.DataFrame, aggregation: str = 'sum') -> pd.DataFrame:
    """
    Backward analysis: Input Sector → Output Sector
    Calculate total output for each input sector
    
    Parameters
    ----------
    df : pd.DataFrame
        Filtered transaction dataframe
    aggregation : str
        Aggregation function: 'sum', 'mean', 'median', 'max', 'min'
        
    Returns
    -------
    pd.DataFrame
        Backward analysis results
    """
    if len(df) == 0:
        return pd.DataFrame()
    
    # Group by input and output sectors (reversed from forward)
    groupby_cols = ['input_sector_code', 'input_sector_name']
    
    # Check if regional data exists
    if 'input_region' in df.columns and df['input_region'].notna().any():
        groupby_cols.insert(0, 'input_region')
    
    groupby_cols.extend(['output_sector_code', 'output_sector_name'])
    
    if 'output_region' in df.columns and df['output_region'].notna().any():
        groupby_cols.insert(len(groupby_cols)-2, 'output_region')
    
    # Apply aggregation
    result = df.groupby(groupby_cols)['value'].agg(aggregation).reset_index()
    result.columns = groupby_cols + ['value']
    
    # Sort by input sector and value (descending)
    sort_cols = [col for col in groupby_cols if 'region' not in col][:2]
    result = result.sort_values(sort_cols + ['value'], ascending=[True, True, False])
    
    return result


def get_sector_summary(df: pd.DataFrame) -> Dict:
    """
    Get summary statistics for analysis
    
    Parameters
    ----------
    df : pd.DataFrame
        Analysis results dataframe
        
    Returns
    -------
    dict
        Summary statistics
    """
    if len(df) == 0:
        return {'total_records': 0, 'total_value': 0}
    
    return {
        'total_records': len(df),
        'total_value': df['value'].sum(),
        'mean_value': df['value'].mean(),
        'max_value': df['value'].max(),
        'min_value': df['value'].min(),
    }


def save_results(results: Dict, output_dir: str = 'analysis_results') -> None:
    """
    Save analysis results to CSV files
    
    Parameters
    ----------
    results : dict
        Dictionary with keys 'forward' and/or 'backward' containing DataFrames
    output_dir : str
        Output directory path
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    if 'forward' in results and len(results['forward']) > 0:
        forward_path = output_path / 'forward_analysis.csv'
        results['forward'].to_csv(forward_path, index=False, encoding='utf-8-sig')
        print(f"✓ Saved forward analysis to {forward_path}")
    
    if 'backward' in results and len(results['backward']) > 0:
        backward_path = output_path / 'backward_analysis.csv'
        results['backward'].to_csv(backward_path, index=False, encoding='utf-8-sig')
        print(f"✓ Saved backward analysis to {backward_path}")


def run_analysis(config_path: str = 'config.json') -> Dict:
    """
    Run complete analysis pipeline based on config

    Parameters
    ----------
    config_path : str
        Path to config.json file

    Returns
    -------
    dict
        Analysis results with 'forward', 'backward', and 'summary' keys
    """
    # Load configuration
    config = load_config(config_path)
    
    # Load data
    df_trans, df_index = load_data(config)
    
    if config.get('output', {}).get('verbose'):
        print("Data loaded successfully")
        print(f"  Transaction records: {len(df_trans)}")
        print(f"  Index sectors: {len(df_index)}")
    
    # Apply filters
    df_filtered = apply_filters(df_trans, config)
    
    if config.get('output', {}).get('verbose'):
        print(f"After filtering: {len(df_filtered)} records")
    
    # Run analysis based on direction
    results = {}
    aggregation = config['analysis'].get('aggregation', 'sum')
    direction = config['analysis'].get('direction', 'both')
    
    if direction in ['forward', 'both']:
        results['forward'] = analyze_forward(df_filtered, aggregation)
        results['forward_summary'] = get_sector_summary(results['forward'])
        
        if config.get('output', {}).get('verbose'):
            print(f"\nForward Analysis:")
            print(f"  Records: {results['forward_summary']['total_records']}")
            print(f"  Total value: {results['forward_summary']['total_value']:,.2f}")
    
    if direction in ['backward', 'both']:
        results['backward'] = analyze_backward(df_filtered, aggregation)
        results['backward_summary'] = get_sector_summary(results['backward'])
        
        if config.get('output', {}).get('verbose'):
            print(f"\nBackward Analysis:")
            print(f"  Records: {results['backward_summary']['total_records']}")
            print(f"  Total value: {results['backward_summary']['total_value']:,.2f}")
    
    # Save results if configured
    if config.get('output', {}).get('save_results'):
        save_results(results, config['output'].get('output_directory', 'analysis_results'))
    
    return results

