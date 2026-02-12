# Quick Start Guide

## Two-Command Setup

### Step 1: Convert Data (One Time)
```bash
python3 converter.py
```
Converts raw Excel files to clean CSV format.

**Output:**
- `data/io_index_dataframe.csv` - Sector index
- `data/io_transaction_dataframe.csv` - Transaction data

### Step 2: Run Analysis
```bash
python3 main.py
```
Performs analysis based on `config.json`.

**Output:**
- `analysis_results/forward_analysis.csv` - Downstream (Output→Input)
- `analysis_results/backward_analysis.csv` - Upstream (Input→Output)

### Step 3: Calculate Economic Impact (Optional)
```bash
# First run main.py, then calculate economic impact
python3 calculate_impact.py
```
Calculates economic impact with specific input amount (default: 1 million KRW).

**Output:**
- `analysis_results/economic_impact.csv` - Impact values with input multiplied

## Customize Analysis

Edit `config.json` and change filters:

### Example: National Data Only
```json
{
  "filters": {
    "geographical_level": "national"
  }
}
```

### Example: Specific Sectors
```json
{
  "filters": {
    "output_sectors": ["0111", "0112", "0121"]
  }
}
```

### Example: Regional Seoul Only
```json
{
  "filters": {
    "geographical_level": "regional",
    "output_region": "서울"
  }
}
```

Then run: `python3 main.py`

## File Structure
```
Root:              converter.py, main.py, config.json
Functions:         libs/io_table_converter.py, libs/io_analyzer.py
Documentation:     doc/*.md
Output Data:       data/*.csv
Analysis Results:  analysis_results/*.csv
```

## No Functions in Main Scripts
✓ converter.py - Only calls functions
✓ main.py - Only calls functions
✓ All functions in libs/
✓ All config in config.json (JSON format)

## Next: GUI
When you add GUI later:
1. GUI edits config.json
2. GUI calls `python3 main.py`
3. GUI reads analysis_results/*.csv

Configuration system is ready!

