"""
Sector Finder Library
Finds sector codes by sector name keyword
"""

import pandas as pd


def find_sector_by_name(sector_name_keyword):
    """
    Find sector codes that match a keyword

    Parameters
    ----------
    sector_name_keyword : str
        Keyword to search for (e.g., "철강" for steel)

    Returns
    -------
    pd.DataFrame
        Matching sectors with codes and names
    """
    df_index = pd.read_csv(
        'data/io_index_dataframe.csv',
        encoding='utf-8-sig'
    )

    # Search for sector name containing keyword
    mask = df_index['sector_name'].str.contains(sector_name_keyword, na=False)
    results = df_index[mask][['sector_code', 'sector_name', 'sector_type', 'geographical_level']].drop_duplicates()
    results = results.sort_values('sector_code')

    return results
