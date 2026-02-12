"""
IO Table Analysis - Main Menu Entry Point

Single entry point that lets users choose which operation to run:
1. Data Conversion (converter.py)
2. IO Table Analysis (io_analyzer.py)
3. Economic Impact Calculation (calculate_impact.py)
4. Find Sector Codes (find_sectors.py)
"""

from libs.converter import run_conversion
from libs.io_analyzer import run_analysis
from libs.calculate_impact import run_impact_calculation
from libs.find_sectors import run_sector_finder


def show_menu():
    """
    Display main menu and return user choice
    """
    print("\n" + "="*70)
    print("IO Table Analysis System")
    print("="*70)
    print("""
Operations:

1. Convert Data
   Convert raw Excel files to clean CSV format
   (One-time setup: creates data/io_*.csv files)

2. Run Analysis
   Analyze IO tables with filters and aggregation
   (Uses config.json for settings)

3. Calculate Economic Impact
   Calculate sector impact with specific input amount
   (Requires: run option 2 first)

4. Find Sector Codes
   Search for sector codes by name keyword
   (Useful for setting up config.json filters)

0. Exit
""")
    choice = input("Select operation (0-4): ").strip()
    return choice


def main():
    """
    Main menu loop
    """
    while True:
        choice = show_menu()

        if choice == "1":
            print("\n" + "="*70)
            print("Starting Data Conversion")
            print("="*70)
            run_conversion()

        elif choice == "2":
            print("\n" + "="*70)
            print("Starting IO Table Analysis")
            print("="*70)
            run_analysis('config.json')

        elif choice == "3":
            print("\n" + "="*70)
            print("Starting Economic Impact Calculation")
            print("="*70)
            run_impact_calculation()

        elif choice == "4":
            print("\n" + "="*70)
            print("Starting Sector Finder")
            print("="*70)
            run_sector_finder()

        elif choice == "0":
            print("\n" + "="*70)
            print("Goodbye!")
            print("="*70)
            break

        else:
            print("\n⚠ Invalid choice. Please select 0-4.")

        # Ask to continue
        cont = input("\nPress Enter to continue or 'q' to quit: ").strip().lower()
        if cont == 'q':
            print("\n" + "="*70)
            print("Goodbye!")
            print("="*70)
            break


if __name__ == '__main__':
    main()
