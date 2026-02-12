# IO Table Project - Final Structure

## Complete Project Layout

```
iotable/
│
├── ROOT DIRECTORY
│   ├── main.py                  ← Analysis entry point (functions calls only)
│   ├── converter.py             ← Data conversion (functions calls only)
│   ├── config.json              ← User configuration (JSON format)
│   └── README.md
│
├── libs/                         ← Function libraries
│   ├── __init__.py
│   ├── io_table_converter.py   ← Conversion functions (English comments)
│   └── io_analyzer.py          ← Analysis functions (English comments)
│
├── doc/                          ← Documentation
│   ├── README_IO_CONVERTER.md
│   ├── PROJECT_STRUCTURE.md
│   ├── LANGUAGE_CONVERSION.md
│   ├── IO_ANALYZER_GUIDE.md
│   └── FINAL_STRUCTURE.md        ← This file
│
├── data/                         ← Output data (generated)
│   ├── io_index_dataframe.csv
│   └── io_transaction_dataframe.csv
│
├── analysis_results/             ← Analysis output (generated)
│   ├── forward_analysis.csv
│   └── backward_analysis.csv
│
└── rawdata/                      ← Input data (raw Excel files)
    └── *.xlsx files
```

## Key Design Principles

### 1. Separation of Concerns
- **main.py** - Only function calls, no function definitions
- **converter.py** - Only function calls, no function definitions
- **libs/** - All function definitions and business logic
- **config.json** - All user inputs separated from code

### 2. Two-Step Workflow

#### Step 1: Data Conversion (converter.py)
```
Raw Excel Files (rawdata/)
        ↓
converter.py (calls io_table_converter functions)
        ↓
Clean Data Files (data/*.csv)
```

#### Step 2: Analysis (main.py)
```
Config (config.json) + Clean Data (data/*.csv)
        ↓
main.py (calls io_analyzer functions)
        ↓
Analysis Results (analysis_results/*.csv)
```

### 3. Function Organization

**libs/io_table_converter.py** (for data conversion)
- `create_sample_io_table()` - Create sample data
- `wide_to_long_sample()` - Convert sample data
- `validate_conversion()` - Validate conversion
- `identify_summary_rows()` - Identify summary rows
- `identify_summary_columns()` - Identify summary columns
- `clean_io_table()` - Clean data
- `io_table_to_long()` - Convert to long format
- `detect_geographical_level()` - Detect region/national
- `process_excel_file()` - Process Excel files
- `create_index_dataframe()` - Create index
- `create_transaction_dataframe()` - Create transactions

**libs/io_analyzer.py** (for analysis)
- `load_config()` - Load JSON config
- `load_data()` - Load CSV data
- `apply_filters()` - Apply all filters
- `analyze_forward()` - Downstream analysis
- `analyze_backward()` - Upstream analysis
- `get_sector_summary()` - Get statistics
- `save_results()` - Save to CSV
- `run_analysis()` - Main pipeline

### 4. Configuration System

**config.json** contains:
```
data_source         ← File paths
filters             ← All filtering options
analysis            ← Direction, aggregation
output              ← Save settings, verbosity
```

Ready for GUI integration - GUI will just generate config.json files!

## Usage Workflows

### Workflow 1: Initial Data Conversion
```bash
# One-time conversion from raw Excel to CSV
python3 converter.py
```

Output: `data/io_index_dataframe.csv`, `data/io_transaction_dataframe.csv`

### Workflow 2: Analysis
```bash
# Edit config.json with your filters
nano config.json

# Run analysis
python3 main.py
```

Output: `analysis_results/forward_analysis.csv`, `analysis_results/backward_analysis.csv`

## Design Benefits

✅ **Clean Code**
- No function definitions in main scripts
- All logic in libs/
- Configuration separated from code

✅ **Reusability**
- Functions can be imported and used elsewhere
- Config format is language-agnostic

✅ **Maintainability**
- Easy to find and modify functions
- Config changes don't require code changes
- English comments throughout

✅ **Scalability**
- Ready for GUI application
- Can add more analyzers (io_forecaster.py, io_validator.py, etc.)
- Config system extends easily

✅ **Testing**
- Each function can be tested independently
- Config can be version controlled
- Results are reproducible

## Future Extensions

### Add More Analyzers
```
libs/
├── io_table_converter.py    ✓ Done
├── io_analyzer.py           ✓ Done
├── io_forecaster.py         ← Future
├── io_validator.py          ← Future
└── io_visualizer.py         ← Future
```

### Add GUI Application
```
gui/
├── config_editor.py         ← Edit config.json
├── result_viewer.py         ← View results
└── visualization.py         ← Plot results
```

### Add API Server
```
api/
├── server.py               ← Flask/FastAPI
├── endpoints.py            ← API routes
└── utils.py               ← Helpers
```

## Configuration Examples

See `doc/IO_ANALYZER_GUIDE.md` for detailed examples:
1. National data analysis
2. Regional analysis (Seoul)
3. Specific table with threshold
4. Multi-region comparison

## Language and Data

✓ **Code Comments**: English (all)
✓ **Data Values**: Korean (preserved, 한국어)
✓ **Output Labels**: English
✓ **Sector Names**: Korean (original language)

Example output:
```
output_sector_name: 철강 (kept in Korean)
input_sector_name: 전력 (kept in Korean)
```

