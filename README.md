# Input-Output Table Analysis Tool

A command-line interface (CLI) tool for analyzing economic impacts using Input-Output (I-O) tables. This tool provides comprehensive analysis of inter-industry relationships, economic multipliers, and sector linkages based on Korean I-O table data.

## Features

### Core Analysis Capabilities

- **Direct Effects Analysis**: Calculate economic impacts for individual sectors
- **Multi-coefficient Analysis**: Support for multiple coefficient types
  - Indirect Production (Leontief inverse)
  - Indirect Import effects
  - Value-Added effects
  - Job Creation coefficients
  - Direct Employment coefficients
- **Sector Aggregation**: Aggregate results by product categories (code_h)
- **Advanced Metrics**:
  - Forward and backward linkages
  - Economic multipliers (output, value-added, employment)
  - Key sector identification
  - Sector comparison analysis
  - Sensitivity analysis

### User-Friendly CLI Interface

- Interactive menu-driven interface
- Clear prompts and formatted output
- Flexible sector selection (by code or name)
- Export results to Excel or CSV formats

## Installation

### Requirements

Python 3.8 or higher is recommended.

```bash
pip install -r requirements.txt
```

Or install dependencies manually:

```bash
pip install pandas numpy openpyxl
```

### Dependencies

- **pandas**: Data processing and analysis
- **numpy**: Numerical computations
- **openpyxl**: Excel file handling

## Quick Start

### Running the Application

```bash
python main.py
```

The application will prompt you to select an I-O table file. Press Enter to use the default (`data/iotable_2020.xlsx`) or provide a custom path.

### Basic Workflow

1. **Launch the application**
2. **Select an I-O table** (default or custom)
3. **Choose an analysis option** from the menu (1-11)
4. **Follow the prompts** to input parameters
5. **View results** in the terminal
6. **Export results** if needed (option 10)

## Menu Options

### Basic Analysis

1. **List all sectors**: Display all available sectors in the I-O table
2. **Analyze single effect**: Calculate impacts for one coefficient type
3. **Analyze all effects**: Calculate impacts across all coefficient types
4. **Aggregate by category**: Group results by product categories (code_h)

### Advanced Analysis

5. **Calculate linkages**: Compute forward and backward linkages for sectors
6. **Calculate multipliers**: Determine output, value-added, and employment multipliers
7. **Compare sectors**: Compare economic impacts across multiple sectors
8. **Identify key sectors**: Find sectors with high linkage values
9. **Sensitivity analysis**: Test how impacts vary with different demand changes

### Utilities

10. **Export results**: Save analysis results to Excel or CSV files
11. **Exit**: Close the application

## Analysis Types

### Coefficient Types

| Coefficient Type | Description | Unit | Variable Name |
|-----------------|-------------|------|---------------|
| Indirect Production | Production induced by demand changes (Leontief inverse) | Million Won | `indirect_prod` |
| Indirect Import | Import requirements induced by demand changes | Million Won | `indirect_import` |
| Value Added | GDP contribution from demand changes | Million Won | `value_added` |
| Job Creation | Total employment created | Persons | `jobcoeff` |
| Direct Employment | Direct jobs in affected sectors | Persons | `directemploycoeff` |

### Linkage Analysis

- **Backward Linkage**: Measures how much a sector demands from other sectors
- **Forward Linkage**: Measures how much other sectors demand from this sector
- **Key Sectors**: Sectors with both high backward and forward linkages (normalized > 1.0)

### Multiplier Analysis

- **Output Multiplier**: Total output generated per unit of final demand
- **Value-Added Multiplier**: Total GDP generated per unit of final demand
- **Employment Multiplier**: Total jobs created per unit of final demand

## Data Files

### Required Data Structure

I-O table Excel files must contain the following sheets:

- **basicmap**: Mapping of sector codes to names and categories
- **indirectprodcoeff**: Indirect production coefficients
- **indirectimportcoeff**: Indirect import coefficients
- **valueaddedcoeff**: Value-added coefficients
- **jobcoeff**: Job creation coefficients (optional)
- **directemploycoeff**: Direct employment coefficients (optional)
- **subsectormap**: Sub-sector mapping for employment analysis (optional)

### Included Data

- **`data/iotable_2020.xlsx`**: Korean Input-Output Table 2020 (380+ sectors)

## Usage Examples

### Example 1: Analyze Production Effects

```
Select option: 2
Select type: indirect_prod
Enter sector code: 1610
Enter demand change: 1000000
```

This calculates the indirect production effects of a 1 billion won increase in sector 1610.

### Example 2: Compare Multiple Sectors

```
Select option: 7
Sectors: 1610, 4506
Enter demand change: 1000000
Coefficient type: value_added
```

This compares the value-added impacts of a 1 billion won increase in sectors 1610 and 4506.

### Example 3: Identify Key Sectors

```
Select option: 8
Enter threshold: 1.0
```

This identifies all sectors with normalized backward and forward linkages above 1.0.

### Example 4: Sensitivity Analysis

```
Select option: 9
Enter sector code: 1610
Values: 100000, 500000, 1000000, 5000000
Coefficient type: indirect_prod
```

This tests how production impacts vary across different demand change scenarios.

## Project Structure

```
iotable/
├── main.py                    # Main CLI application
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── libs/                      # Core library modules
│   ├── __init__.py            # Package initialization
│   ├── io_analyzer.py         # I-O table analysis engine
│   └── wrapper.py             # CLI menu handlers
│
└── data/                      # Data files
    └── iotable_2020.xlsx      # Korean I-O Table 2020
```

## Analysis Methodology

### Economic Impact Formula

```
Impact = Coefficient Matrix × Demand Change Vector

For sector i:
Impact_i = Σ(C_ij × ΔD_j)

Where:
- C_ij: Coefficient from sector j to sector i
- ΔD_j: Demand change in sector j
```

### Linkage Calculation

```
Backward Linkage_j = Σ_i (L_ij) / n
Forward Linkage_i = Σ_j (L_ij) / n

Normalized Linkage = Linkage / Average(All Linkages)

Where:
- L_ij: Leontief inverse coefficient
- n: Number of sectors
```

### Multiplier Calculation

```
Output Multiplier_j = Σ_i (L_ij)
Value-Added Multiplier_j = Σ_i (V_i × L_ij)
Employment Multiplier_j = Σ_i (E_i × L_ij)

Where:
- V_i: Value-added coefficient for sector i
- E_i: Employment coefficient for sector i
```

## Export Formats

### Excel Export (.xlsx)
- Formatted tables with headers
- Separate sheets for different result types
- Metadata included (analysis parameters, dates)

### CSV Export (.csv)
- UTF-8 with BOM encoding (Korean text support)
- Compatible with Excel and other spreadsheet applications

## Technical Details

### Sector Code Format

- Basic sectors: 4-digit codes (e.g., "0111", "1610", "4506")
- Sub-sectors: 3-digit codes (e.g., "001", "165")
- Product categories: code_h classification

### Data Processing

- Uses pandas for efficient data manipulation
- Supports large I-O tables (380+ sectors)
- Optimized matrix operations with numpy

## Troubleshooting

### Common Issues

**Error: File not found**
- Ensure the I-O table file exists in the specified path
- Check that the file path is correct

**Error: Invalid sector code**
- Verify the sector code exists in the I-O table
- Use option 1 to list all available sectors

**Error: Sheet not found**
- Ensure the Excel file contains all required sheets
- Check sheet names match expected format

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Support

For questions or issues, please open an issue on the project repository.
