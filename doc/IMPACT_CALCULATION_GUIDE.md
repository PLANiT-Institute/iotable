# Economic Impact Calculation Guide

## Overview

This guide explains how to calculate the economic impact of injecting money into a specific sector using production coefficient tables.

## Concept: Production Coefficient Analysis

**Production Coefficient (생산유발계수):**
- Measures how much economic output is generated in sector B when sector A increases output by 1 unit
- Example: Steel coefficient of 0.5 in Automotive means: when Automotive increases output by 1 KRW, it generates 0.5 KRW of economic activity in Steel

**Impact Calculation:**
```
Economic Impact = Production Coefficient × Input Amount
```

If 1 million KRW is injected into Steel sector in Gyeongnam:
```
Impact on Automotive = 0.5 × 1,000,000 = 500,000 KRW
```

## Step-by-Step Workflow

### Step 1: Find Your Sector Code

First, identify the exact sector code for your analysis target:

```bash
python3 find_sectors.py
```

Enter the sector name keyword (e.g., "철강" for steel):

```
Found 5 sectors containing '철강':
sector_code  sector_name       sector_type  geographical_level
1200         철강              output       regional
1200         철강              input        regional
1201         철강제품          output       regional
...
```

Note the sector code (e.g., "1200" for steel).

### Step 2: Configure Analysis

Edit `config.json` to specify:
- The sector to inject money into (input_sector)
- The region (input_region)
- Production coefficient table (tables)
- Direction: "backward" to see which sectors are impacted

**Example: Steel in Gyeongnam**

```json
{
  "data_source": {
    "transaction_data_path": "data/io_transaction_dataframe.csv",
    "index_data_path": "data/io_index_dataframe.csv"
  },
  "filters": {
    "geographical_level": "regional",
    "tables": ["생산유발계수"],
    "input_region": "경남",
    "input_sectors": ["1200"],
    "output_region": null,
    "output_sectors": null,
    "min_value": null,
    "max_value": null
  },
  "analysis": {
    "direction": "backward",
    "aggregation": "sum"
  },
  "output": {
    "save_results": true,
    "output_directory": "analysis_results",
    "verbose": true
  }
}
```

### Step 3: Run Analysis

```bash
python3 main.py
```

This generates `analysis_results/backward_analysis.csv` containing:
- `input_sector_code`: The sector you injected money into (e.g., 1200 - Steel)
- `input_sector_name`: The sector name (철강 - Steel)
- `input_region`: The region (경남 - Gyeongnam)
- `output_sector_code`: Sectors that use this input
- `output_sector_name`: Names of downstream sectors
- `value`: Production coefficient (how much impact per 1 KRW input)

### Step 4: Calculate Economic Impact

```bash
python3 calculate_impact.py
```

This multiplies the production coefficients by your input amount (default: 1 million KRW) and generates:
- Console output showing impact by sector
- `analysis_results/economic_impact.csv` with detailed results

**Example output:**

```
================================================================================
Economic Impact Analysis: Steel (철강) Input in Gyeongnam (경남)
Input Amount: 1,000,000 KRW
================================================================================

Output Sector: 자동차 (Automobiles) (3200)
  Production Coefficient: 0.25
  Economic Impact: 250,000 KRW

Output Sector: 반도체 (Semiconductors) (3410)
  Production Coefficient: 0.15
  Economic Impact: 150,000 KRW

Output Sector: 철강제품 (Steel Products) (1201)
  Production Coefficient: 0.45
  Economic Impact: 450,000 KRW

================================================================================
Total Economic Impact: 1,200,000 KRW
Affected Sectors: 23
================================================================================
```

## Different Input Amounts

To calculate impact for different input amounts, modify the Python script:

```python
# Calculate impact for 10 million KRW instead of 1 million
results = calculate_economic_impact(input_amount_kwon=10000000)
```

Or edit the script directly:

```python
if __name__ == '__main__':
    results = calculate_economic_impact(input_amount_kwon=10000000)  # 10 million KRW
```

## Analysis Variations

### Variation 1: Employment Impact
If you have employment coefficient data instead:

```json
{
  "filters": {
    "tables": ["고용유발계수"],
    "input_sectors": ["1200"]
  }
}
```

Then employment impact = coefficient × input amount (e.g., 0.05 jobs per 1 million KRW)

### Variation 2: Multiple Sectors
Analyze impact of injecting into multiple input sources:

```json
{
  "filters": {
    "input_sectors": ["1200", "2100", "3200"]
  }
}
```

Then run analysis separately for each or compare results.

### Variation 3: Different Regions
Compare impact across different regions:

```json
{
  "filters": {
    "geographical_level": "regional",
    "input_sectors": ["1200"]
  }
}
```

This returns impact in all regions. Then calculate impact for each region separately:

```python
df_impact = pd.read_csv('analysis_results/backward_analysis.csv', encoding='utf-8-sig')

# Calculate impact for each region separately
for region in df_impact['input_region'].unique():
    df_region = df_impact[df_impact['input_region'] == region]
    region_impact = (df_region['value'] * 1000000).sum()
    print(f"{region}: {region_impact:,.0f} KRW")
```

## Key Files

| File | Purpose |
|------|---------|
| `config.json` | Main configuration (edit before running analysis) |
| `main.py` | Run analysis based on config.json |
| `calculate_impact.py` | Calculate economic impact with input amount |
| `find_sectors.py` | Find sector codes by sector name |
| `analysis_results/backward_analysis.csv` | Raw production coefficients |
| `analysis_results/economic_impact.csv` | Calculated impact values |

## Troubleshooting

**Q: No results found?**
- Check sector code is correct: Run `find_sectors.py`
- Verify the sector exists in the region: Try `"geographical_level": null` to see all regions
- Check table name is exact: Common tables are "생산유발계수", "고용유발계수"

**Q: Impact values too small/large?**
- Confirm input amount is in correct units (KRW, not thousand KRW)
- Production coefficients are typically small (0.01-0.5)
- Impact = coefficient × input, so check both values

**Q: Want to analyze forward direction?**
- Change direction from "backward" to "forward"
- This shows what inputs sector needs, not which sectors are impacted
- Less useful for impact analysis

## Example: Complete Workflow

```bash
# Step 1: Find steel sector code
python3 find_sectors.py
# Enter: 철강
# Output: sector_code 1200

# Step 2: Edit config.json with sector 1200 (already done above)
nano config.json

# Step 3: Run analysis
python3 main.py

# Step 4: Calculate impact with 1 million KRW
python3 calculate_impact.py

# Step 5: View results
cat analysis_results/economic_impact.csv
```

## Next Steps

- Modify `calculate_impact.py` for different input amounts or sector codes
- Create multiple config files for different scenarios (config_steel.json, config_auto.json, etc.)
- Integrate with GUI application for interactive analysis
