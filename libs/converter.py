"""
Korean Input-Output (IO) Table Data Conversion Library
- Convert wide-format to long-format
- Process sample data and real data
- Separate regional/national data
"""

from .io_table_converter import (
    create_sample_io_table,
    wide_to_long_sample,
    validate_conversion,
    process_excel_file,
    create_index_dataframe,
    create_transaction_dataframe
)

from pathlib import Path
import pandas as pd


def run_conversion():
    """
    Main execution function
    """

    print("\n" + "="*70)
    print("한국 투입산출표 데이터 변환 스크립트")
    print("="*70)

    # ========== Sample data processing ==========
    print("\n\n" + "="*70)
    print("[PART 1] Sample data processing")
    print("="*70)

    # Generate sample data
    df_wide_sample = create_sample_io_table()

    # Convert to long format
    df_long_sample = wide_to_long_sample(df_wide_sample)

    # Validate
    validate_conversion(df_wide_sample, df_long_sample)

    # ========== Real data processing ==========
    print("\n\n" + "="*70)
    print("[PART 2] Real data processing (rawdata folder)")
    print("="*70)

    rawdata_path = Path('rawdata')

    if not rawdata_path.exists():
        print(f"\n⚠ Warning: {rawdata_path} folder not found.")
        print("Show example of CSV/Excel file loading instead.")

        print("\n[CSV file loading example]")
        print("""
# CSV 파일 (Wide format)
df = pd.read_csv('io_table.csv', index_col=0)

# Excel 파일 (특정 시트)
df = pd.read_excel('io_table.xlsx', sheet_name='거래표', header=5)

# Convert to long format
df_long = df.reset_index().melt(
    id_vars=['sector_name'],
    var_name='input_sector',
    value_name='value'
)
        """)
    else:
        print(f"\n{rawdata_path} 폴더의 Processing Excel files...")

        excel_files = list(rawdata_path.glob('*.xlsx'))
        print(f"Excel files found: {len(excel_files)}개")

        all_data = []
        all_stats = []

        # Process main files (처음 3개 파일)
        for file_path in excel_files[:3]:
            df_long, stats = process_excel_file(str(file_path))
            all_data.append(df_long)
            all_stats.append(stats)

        if all_data:
            # Combine all dataframes
            df_combined_long = pd.concat(all_data, ignore_index=True)

            print(f"\nTotal combined data: {len(df_combined_long):,} 행")

            # 샘플링 (대용량 데이터 처리 시)
            if len(df_combined_long) > 1000000:
                print(f"Large dataset detected (> 1백만 행)")
                print("Sampling top 10,000 rows per sheet to reduce processing time...")

                # 시트별로 샘플링 (테이블별로 샘플링)
                sampled_data = []
                table_col = 'table' if 'table' in df_combined_long.columns else 'source_sheet'
                for table_name in df_combined_long[table_col].unique():
                    sheet_data = df_combined_long[df_combined_long[table_col] == table_name]
                    sheet_sample = sheet_data.head(10000)
                    sampled_data.append(sheet_sample)

                df_combined_long = pd.concat(sampled_data, ignore_index=True)
                print(f"Data after sampling: {len(df_combined_long):,} 행\n")

            # 두 가지 길형식 데이터프레임 생성
            print("\n" + "-"*70)
            print("Creating index dataframe...")
            df_index = create_index_dataframe(df_combined_long)
            print(f"✓ Complete: {len(df_index):,} sectors/products")
            print(df_index.head(10))

            print("\n" + "-"*70)
            print("Creating transaction dataframe...")
            df_transaction = create_transaction_dataframe(df_combined_long)
            print(f"✓ Complete: {len(df_transaction):,} transaction records")
            print(df_transaction.head(10))

            # CSV로 저장
            print("\n" + "-"*70)
            print("Saving results...")

            # data Create folder (if not exists)
            data_dir = Path('data')
            data_dir.mkdir(exist_ok=True)

            index_path = data_dir / 'io_index_dataframe.csv'
            transaction_path = data_dir / 'io_transaction_dataframe.csv'

            df_index.to_csv(index_path, index=False, encoding='utf-8-sig')
            df_transaction.to_csv(transaction_path, index=False, encoding='utf-8-sig')

            print(f"✓ {index_path}")
            print(f"✓ {transaction_path}")

    # ========== 최종 요약 ==========
    print("\n\n" + "="*70)
    print("처리 Complete")
    print("="*70)
    print("""
Output:
1. data/io_index_dataframe.csv: 실제 데이터 인덱스
2. data/io_transaction_dataframe.csv: 실제 데이터 거래 기록

Features:
✓ Remove all summary rows/columns
✓ Keep original language (Korean)
✓ Use English column names
✓ Separate regional/national data
✓ Include input region and sector names
✓ Automatically combine multiple sheets

Documentation: doc/README_IO_CONVERTER.md
    """)
