"""
Sector Finder Module
Wrapper that calls sector_finder functions
Useful for setting up config.json filters
"""

from .sector_finder import find_sector_by_name


def run_sector_finder():
    """
    Run sector finder to search for sector codes by name
    """
    print("\n" + "="*70)
    print("Find Sector Codes")
    print("="*70)

    keyword = input("Enter sector name keyword (e.g., 철강): ").strip()

    if keyword:
        results = find_sector_by_name(keyword)

        if len(results) > 0:
            print(f"\nFound {len(results)} sectors containing '{keyword}':")
            print(results.to_string(index=False))
            print("\n✓ Copy the sector_code values to use in config.json 'input_sectors' or 'output_sectors'")
        else:
            print(f"No sectors found containing '{keyword}'")
    else:
        print("No keyword provided")
