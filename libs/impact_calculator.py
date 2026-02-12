"""
Economic Impact Calculation Library
Calculates economic impact of sector input based on analysis results
"""

import pandas as pd


def calculate_economic_impact(input_amount_kwon=1000000, direction="forward"):
    """
    Calculate economic impact based on analysis direction

    Parameters
    ----------
    input_amount_kwon : float
        Input amount in Korean Won (default: 1,000,000 KRW)
    direction : str
        Analysis direction: "forward" or "backward"

    Returns
    -------
    pd.DataFrame
        Economic impact results
    """
    # Load analysis results
    if direction == "forward":
        csv_file = 'analysis_results/forward_analysis.csv'
        title = "Economic Impact of Steel (철강) Production in Gyeongnam (경남)"
        sector_col = 'input_sector_name'
        region_col = 'input_region'
    else:  # backward
        csv_file = 'analysis_results/backward_analysis.csv'
        title = "Sectors Using Steel (철강) Input from Gyeongnam (경남)"
        sector_col = 'output_sector_name'
        region_col = 'output_region'

    df_impact = pd.read_csv(csv_file, encoding='utf-8-sig')

    # The 'value' column contains production coefficient
    # impact = production_coefficient × input_amount
    df_impact['economic_impact_kwon'] = df_impact['value'] * input_amount_kwon

    # Sort by impact (descending)
    df_impact = df_impact.sort_values('economic_impact_kwon', ascending=False)

    # Display results
    print("\n" + "="*80)
    print(title)
    print(f"Input Amount: {input_amount_kwon:,.0f} KRW")
    print("="*80)
    print()

    if direction == "forward":
        print("Sectors that provide INPUTS to Steel production:")
        for idx, row in df_impact.iterrows():
            region_info = f" ({row['input_region']})" if pd.notna(row.get('input_region')) else ""
            print(f"  • {row['input_sector_name']}{region_info} (Code: {row['input_sector_code']})")
            print(f"    Input Coefficient: {row['value']:.6f}")
            print(f"    Total Input Needed: {row['economic_impact_kwon']:,.0f} KRW")
    else:
        print("Sectors that CONSUME Steel input:")
        for idx, row in df_impact.iterrows():
            region_info = f" ({row['output_region']})" if pd.notna(row.get('output_region')) else ""
            print(f"  • {row['output_sector_name']}{region_info} (Code: {row['output_sector_code']})")
            print(f"    Consumption Coefficient: {row['value']:.6f}")
            print(f"    Total Consumption: {row['economic_impact_kwon']:,.0f} KRW")

    print()

    # Summary
    total_impact = df_impact['economic_impact_kwon'].sum()
    print("="*80)
    print(f"Total Economic Impact: {total_impact:,.0f} KRW")
    print(f"Affected Sectors: {len(df_impact)}")
    print(f"Average Impact per Sector: {(total_impact / len(df_impact)):,.0f} KRW" if len(df_impact) > 0 else "")
    print("="*80)

    # Save results
    df_impact.to_csv('analysis_results/economic_impact.csv', index=False, encoding='utf-8-sig')
    print("\n✓ Saved detailed results to: analysis_results/economic_impact.csv")

    return df_impact
