"""
Economic Impact Calculation Module
Wrapper that calls impact_calculator functions
"""

from .impact_calculator import calculate_economic_impact


def run_impact_calculation():
    """
    Run economic impact calculation with 1 million KRW input
    """
    print("\n" + "="*70)
    print("Economic Impact Calculator")
    print("="*70)

    # Calculate impact with 1 million KRW (forward direction by default)
    results = calculate_economic_impact(input_amount_kwon=1000000, direction="forward")

    print("\n" + "="*70)
    print("Calculation Complete")
    print("="*70)
