# IO Table Analyzer User Guide

## Overview
The IO Analyzer performs bidirectional analysis of input-output tables with full filtering capabilities.

## Structure
```
├── main.py              ← Entry point (function calls only)
├── config.json          ← Configuration (user inputs)
├── libs/
│   └── io_analyzer.py   ← All analysis functions
├── analysis_results/    ← Output directory
│   ├── forward_analysis.csv
│   └── backward_analysis.csv
```

## Quick Start

### 1. Run Default Analysis
```bash
python3 main.py
```

### 2. Customize Analysis
Edit `config.json` and run again:
```json
{
  "filters": {
    "geographical_level": "national",
    "output_sectors": ["0111", "0112"]
  },
  "analysis": {
    "direction": "forward"
  }
}
```

## Configuration Options

### Data Source
```json
"data_source": {
  "transaction_data_path": "data/io_transaction_dataframe.csv",
  "index_data_path": "data/io_index_dataframe.csv"
}
```

### Filters
All filters are **optional** (null = no filter):

**Geographical Level**
```json
"geographical_level": null
// Options: null, "national", "regional"
```

**Table Selection**
```json
"tables": null
// Example: ["A표_총거래표(생산자)", "생산유발계수"]
```

**Regional Filters**
```json
"output_region": null,    // Example: "서울", "강원"
"input_region": null      // Example: "서울", "강원"
```

**Sector Filters**
```json
"output_sectors": null,   // Example: ["0111", "0112", "0121"]
"input_sectors": null     // Example: ["011", "012", "019"]
```

**Value Range**
```json
"min_value": null,        // Example: 1000
"max_value": null         // Example: 100000
```

### Analysis Configuration

**Direction**
```json
"direction": "both"
// Options: "forward", "backward", "both"
```
- **forward**: Output Sector → Input Sector (downstream analysis)
- **backward**: Input Sector → Output Sector (upstream analysis)
- **both**: Calculate both directions

**Aggregation**
```json
"aggregation": "sum"
// Options: "sum", "mean", "median", "max", "min"
```

### Output Configuration
```json
"output": {
  "save_results": true,
  "output_directory": "analysis_results",
  "verbose": true
}
```

## Example Configurations

### Example 1: National Data Analysis
```json
{
  "filters": {
    "geographical_level": "national",
    "output_sectors": ["0111", "0112", "0121"]
  },
  "analysis": {
    "direction": "forward"
  }
}
```

### Example 2: Regional Analysis (Seoul)
```json
{
  "filters": {
    "geographical_level": "regional",
    "output_region": "서울"
  },
  "analysis": {
    "direction": "both"
  }
}
```

### Example 3: Specific Table with Threshold
```json
{
  "filters": {
    "tables": ["A표_총거래표(생산자)"],
    "min_value": 1000
  },
  "analysis": {
    "direction": "backward",
    "aggregation": "mean"
  }
}
```

### Example 4: Multi-Region Comparison
```json
{
  "filters": {
    "geographical_level": "regional"
  },
  "analysis": {
    "direction": "forward",
    "aggregation": "sum"
  }
}
```

## Output Files

### forward_analysis.csv
Output Sector → Input Sector (downstream)

Columns:
- `output_sector_code`: Output sector code
- `output_sector_name`: Output sector name (Korean)
- `output_region`: Region (if applicable)
- `input_sector_code`: Input sector code
- `input_sector_name`: Input sector name (Korean)
- `input_region`: Region (if applicable)
- `value`: Transaction amount (aggregated)

### backward_analysis.csv
Input Sector → Output Sector (upstream)

Columns:
- `input_sector_code`: Input sector code
- `input_sector_name`: Input sector name (Korean)
- `input_region`: Region (if applicable)
- `output_sector_code`: Output sector code
- `output_sector_name`: Output sector name (Korean)
- `output_region`: Region (if applicable)
- `value`: Transaction amount (aggregated)

## Analysis Types

### Forward Analysis (Output → Input)
Answers: "What inputs does sector X need?"

Example output:
```
Output Sector: 철강 (Steel)
├─ Input: 철광석 (Iron ore) - 100,000 units
├─ Input: 전력 (Electricity) - 50,000 units
└─ Input: 석탄 (Coal) - 30,000 units
```

### Backward Analysis (Input → Output)
Answers: "Which sectors use input X?"

Example output:
```
Input Sector: 전력 (Electricity)
├─ Output: 철강 (Steel) - 50,000 units
├─ Output: 자동차 (Automobiles) - 40,000 units
└─ Output: 반도체 (Semiconductors) - 35,000 units
```

## Tips

1. **Start Simple**: Run with default config first
2. **Gradually Filter**: Add filters one at a time
3. **Check Results**: Review CSV files for patterns
4. **Compare Regions**: Set `direction: both` for complete analysis
5. **Adjust Aggregation**: Use `mean` or `median` for normalized data

## Troubleshooting

**No results?**
- Check filters are not too restrictive
- Verify sector codes match your data
- Try removing filters one by one

**Large output files?**
- Use regional filters
- Add minimum value threshold
- Filter specific tables

**Want GUI later?**
- This config system is ready for GUI integration
- All user inputs are in config.json
- GUI will simply generate config.json files

