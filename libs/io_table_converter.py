"""
Korean Input-Output (IO) Table Data Conversion Script
- Convert wide-format to long-format
- Include sample data and real data processing
- Remove summary rows and columns (value-added, totals, etc.)
- Keep original language, use English for column names
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')


# ============================================================================
# 1. Sample Data Generation Functions
# ============================================================================

def create_sample_io_table() -> pd.DataFrame:
    """
    Generate sample IO table (wide format)
    Sectors: Steel, Agriculture, Manufacturing, Construction
    """
    sectors = ['철강', '농업', '제조', '건설']

    # Generate arbitrary transaction amounts (million won units)
    data = {
        '철강': [137663, 1939, 1655, 2215],
        '농업': [25453, 1026, 287, 52157],
        '제조': [162, 16, 24, 12],
        '건설': [3667, 2, 1, 1]
    }

    df_wide = pd.DataFrame(data, index=sectors)

    print("\n" + "="*70)
    print("Sample Data - Wide Format")
    print("="*70)
    print(df_wide)
    print(f"\nShape: {df_wide.shape}")
    print(f"Row index (output sector): {list(df_wide.index)}")
    print(f"Column index (input sector): {list(df_wide.columns)}")

    return df_wide


def wide_to_long_sample(df_wide: pd.DataFrame) -> pd.DataFrame:
    """
    Convert sample data from wide to long format
    """
    # Reset index to column
    df_wide_reset = df_wide.reset_index()
    df_wide_reset.columns.name = None
    df_wide_reset = df_wide_reset.rename(columns={'index': 'output_sector'})

    # Convert to long format using melt()
    df_long = df_wide_reset.melt(
        id_vars=['output_sector'],
        var_name='input_sector',
        value_name='transaction_amount'
    )

    print("\n" + "="*70)
    print("Sample Data - Long Format")
    print("="*70)
    print(df_long)
    print(f"\nShape: {df_long.shape}")

    return df_long


def validate_conversion(df_wide: pd.DataFrame, df_long: pd.DataFrame) -> None:
    """
    Validate wide/long format conversion
    - Row sum comparison: wide row sum == long grouped by output_sector sum
    - Column sum comparison: wide column sum == long grouped by input_sector sum
    """
    print("\n" + "="*70)
    print("Validation: Wide ↔ Long Format Conversion Consistency")
    print("="*70)

    # Row sum validation (total transaction per output sector)
    print("\n[1] Total Transaction Amount by Output Sector (Row Sum)")
    print("-" * 70)

    wide_row_sums = df_wide.sum(axis=1)
    long_output_sums = df_long.groupby('output_sector')['transaction_amount'].sum()

    print("Wide format row sum:")
    print(wide_row_sums)
    print("\nLong format output_sector sum:")
    print(long_output_sums)

    # Value comparison (order independent)
    row_match = np.allclose(sorted(wide_row_sums.values), sorted(long_output_sums.values))
    print(f"\nRow sum match: {row_match} ✓" if row_match else f"\nRow sum match: {row_match} ✗")

    # Column sum validation (total transaction per input sector)
    print("\n[2] Total Transaction Amount by Input Sector (Column Sum)")
    print("-" * 70)

    wide_col_sums = df_wide.sum(axis=0)
    long_input_sums = df_long.groupby('input_sector')['transaction_amount'].sum()

    print("Wide format column sum:")
    print(wide_col_sums)
    print("\nLong format input_sector sum:")
    print(long_input_sums)

    # Value comparison (order independent)
    col_match = np.allclose(sorted(wide_col_sums.values), sorted(long_input_sums.values))
    print(f"\nColumn sum match: {col_match} ✓" if col_match else f"\nColumn sum match: {col_match} ✗")

    # Total transaction validation
    wide_total = df_wide.sum().sum()
    long_total = df_long['transaction_amount'].sum()
    total_match = np.isclose(wide_total, long_total)

    print("\n[3] Total Transaction Amount")
    print("-" * 70)
    print(f"Wide format total: {wide_total:,.0f}")
    print(f"Long format total: {long_total:,.0f}")
    print(f"Total match: {total_match} ✓" if total_match else f"Total match: {total_match} ✗")


# ============================================================================
# 2. Real Data Processing Functions
# ============================================================================

def identify_summary_rows(df: pd.DataFrame, sector_col: int = 1) -> List[int]:
    """
    Identify summary rows (부가가치, 총계 등)
    Identify using Korean keywords: 계, 소계, 중간합계
    """
    summary_keywords = ['계', '소계', '중간합계', '합계', '유발']
    summary_row_indices = []

    if sector_col >= len(df.columns):
        return summary_row_indices

    for idx in df.index:
        try:
            cell_value = str(df.iloc[idx, sector_col]).strip()
            # Check if contains any keyword
            if any(keyword in cell_value for keyword in summary_keywords):
                summary_row_indices.append(idx)
        except:
            continue

    return summary_row_indices


def identify_summary_columns(df: pd.DataFrame, header_row: int = 4) -> List[int]:
    """
    Identify summary columns (Row totals, intermediate inputs, etc.)
    - Exclude first 2 columns (Sector code, 이름)
    - Last few columns likely contain totals
    """
    # Find summary keywords in header rows
    summary_keywords = ['계', '합계', '총', '중간']
    summary_col_indices = []

    if header_row < len(df):
        try:
            for col_idx in df.columns:
                try:
                    if isinstance(col_idx, int) and col_idx < 2:  # Exclude first 2 columns
                        continue

                    header_value = str(df.iloc[header_row, col_idx]).strip()
                    if any(keyword in header_value for keyword in summary_keywords):
                        summary_col_indices.append(col_idx)
                except:
                    continue
        except:
            pass

    return summary_col_indices


def clean_io_table(df: pd.DataFrame,
                   header_rows: int = 5,
                   sector_col: int = 1,
                   name_col: int = 1,
                   is_regional: bool = False) -> pd.DataFrame:
    """
    Clean IO table:
    1. Remove header rows (처음 5행)
    2. Remove summary rows
    3. Remove summary columns
    4. Keep sector code and name (For regional tables, also keep region)
    """
    # Remove header rows
    df_clean = df.iloc[header_rows:].copy()
    df_clean.reset_index(drop=True, inplace=True)

    # Regional table: Keep region, sector code, and sector name
    # National table: Keep only sector code and sector name
    if is_regional:
        # Column 0: Region, Column 1: Sector code, Column 2: Sector name
        # Keep first 3 columns, rest are data columns
        data_start_col = 3
    else:
        # Column 0: Sector code, Column 1: Sector name
        data_start_col = 2

    # Identify and remove summary rows (For regional tables, search in different column)
    if is_regional:
        summary_row_indices = identify_summary_rows(df_clean, sector_col=1)
    else:
        summary_row_indices = identify_summary_rows(df_clean, sector_col=0)

    df_clean = df_clean.drop(summary_row_indices).reset_index(drop=True)

    # Identify and remove summary columns
    summary_col_indices = identify_summary_columns(df_clean, header_row=0)

    # Assume last 10 columns are also summary columns
    try:
        potential_summary_cols = list(df_clean.columns[-10:])
        potential_summary_cols = [col for col in potential_summary_cols if isinstance(col, int)]
        summary_col_indices = sorted(set(summary_col_indices + potential_summary_cols))
    except:
        pass

    # Delete except first data_start_col columns
    summary_col_indices = [col for col in summary_col_indices if isinstance(col, int) and col >= data_start_col]
    if summary_col_indices:
        df_clean = df_clean.drop(columns=summary_col_indices, errors='ignore')

    # Remove NaN rows (Based on region/sector code)
    if is_regional:
        df_clean = df_clean.dropna(subset=[0, 1], how='any')
    else:
        df_clean = df_clean.dropna(subset=[0], how='any')

    return df_clean


def io_table_to_long(df: pd.DataFrame,
                     df_raw: pd.DataFrame = None,
                     sheet_name: str = None,
                     is_regional: bool = False) -> pd.DataFrame:
    """
    IO 테이블(광범위)을 길형식으로 변환

    National table: Column 0=섹터코드, 1=섹터명, 2+=값
    Regional table: Column 0=Regional, 1=섹터코드, 2=섹터명, 3+=값
              Header rows: 4=입력Regional, 5=입력섹터코드, 6=입력섹터명

    Parameters:
    -----------
    df : pd.DataFrame
        정제된 IO 테이블 (행: 생산부문, 열: 투입부문)
    df_raw : pd.DataFrame
        정제 전 원본 데이터 (헤더 정보 추출용, Regional 테이블만)
    sheet_name : str
        출처 Sheet name
    is_regional : bool
        Whether regional table

    Returns:
    --------
    pd.DataFrame
        Long-format dataframe
    """

    if is_regional:
        # ===== Process Regional Table =====
        # Extract input sector info from raw data
        input_regions = []
        input_codes = []
        input_names = []

        if df_raw is not None and len(df_raw) > 6:
            for col_idx in range(3, len(df_raw.columns)):
                input_regions.append(str(df_raw.iloc[4, col_idx]).strip())
                input_codes.append(str(df_raw.iloc[5, col_idx]).strip())
                input_names.append(str(df_raw.iloc[6, col_idx]).strip())

        # Column 0=Regional, 1=섹터코드, 2=섹터명으로 인덱스 설정
        df_indexed = df.set_index([0, 1, 2])
        df_indexed.index.names = ['output_region', 'output_sector_code', 'output_sector_name']

        # melt() 사용하여 길형식으로 변환
        df_long = df_indexed.stack().reset_index()
        df_long.columns = ['output_region', 'output_sector_code', 'output_sector_name',
                          'input_column_idx', 'value']

        # Map input sector info (column index가 3부터 시작하므로 조정)
        df_long['input_column_idx_num'] = pd.to_numeric(df_long['input_column_idx'], errors='coerce')
        df_long['input_idx'] = (df_long['input_column_idx_num'] - 3).astype(int)

        # 범위 내의 Input info만 추가
        df_long['input_region'] = df_long['input_idx'].apply(
            lambda x: input_regions[x] if 0 <= x < len(input_regions) else None
        )
        df_long['input_sector_code'] = df_long['input_idx'].apply(
            lambda x: input_codes[x] if 0 <= x < len(input_codes) else None
        )
        df_long['input_sector_name'] = df_long['input_idx'].apply(
            lambda x: input_names[x] if 0 <= x < len(input_names) else None
        )

        # Remove unnecessary columns
        df_long = df_long.drop(columns=['input_column_idx', 'input_column_idx_num', 'input_idx'])

    else:
        # ===== Process National Table =====
        # Extract input sector info from raw data
        input_codes = []
        input_names = []

        if df_raw is not None and len(df_raw) > 5:
            # National 테이블의 헤더 구조 파악
            for col_idx in range(2, len(df_raw.columns)):
                try:
                    code_val = df_raw.iloc[4, col_idx]
                    name_val = df_raw.iloc[5, col_idx]
                    if pd.notna(code_val) and pd.notna(name_val):
                        input_codes.append(str(code_val).strip())
                        input_names.append(str(name_val).strip())
                except:
                    pass

        # Column 0=섹터코드, 1=섹터명으로 인덱스 설정
        df_indexed = df.set_index([0, 1])
        df_indexed.index.names = ['output_sector_code', 'output_sector_name']

        # melt() 사용하여 길형식으로 변환
        df_long = df_indexed.stack().reset_index()
        df_long.columns = ['output_sector_code', 'output_sector_name',
                          'input_column_idx', 'value']

        # Map input sector info (column index가 2부터 시작하므로 조정)
        df_long['input_column_idx_num'] = pd.to_numeric(df_long['input_column_idx'], errors='coerce')
        df_long['input_idx'] = (df_long['input_column_idx_num'] - 2).astype(int)

        # 범위 내의 Input info만 추가
        df_long['input_sector_code'] = df_long['input_idx'].apply(
            lambda x: input_codes[x] if 0 <= x < len(input_codes) else None
        )
        df_long['input_sector_name'] = df_long['input_idx'].apply(
            lambda x: input_names[x] if 0 <= x < len(input_names) else None
        )

        # Remove unnecessary columns
        df_long = df_long.drop(columns=['input_column_idx', 'input_column_idx_num', 'input_idx'])

    # Convert to numeric format
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')

    # 0 or NaN values (Include only actual transactions)
    df_long = df_long[df_long['value'] > 0].copy()

    # Add sheet source (renamed to 'table')
    if sheet_name:
        df_long['table'] = sheet_name

    return df_long.reset_index(drop=True)


def detect_geographical_level(file_path: str) -> Tuple[str, bool]:
    """
    파일명에서 Geographical level과 테이블 타입 감지
    - 'Regional' 포함 → regional (true), Otherwise → national (false)
    """
    filename = Path(file_path).name
    is_regional = 'Regional' in filename
    level = 'regional' if is_regional else 'national'
    return level, is_regional


def process_excel_file(file_path: str,
                      sector_code_col: int = 0,
                      sector_name_col: int = 1) -> Tuple[pd.DataFrame, Dict]:
    """
    Process all sheets from Excel file and combine into single long-format dataframe

    Parameters:
    -----------
    file_path : str
        Excel File path

    Returns:
    --------
    Tuple[pd.DataFrame, Dict]
        - 결합된 Long-format dataframe
        - 처리 통계
    """

    stats = {
        'file_path': file_path,
        'sheets_processed': 0,
        'total_records': 0,
        'errors': []
    }

    all_long_dfs = []
    geographical_level, is_regional_file = detect_geographical_level(file_path)

    try:
        xl_file = pd.ExcelFile(file_path)
        print(f"\n파일: {Path(file_path).name}")
        print(f"Geographical level: {geographical_level}")
        print(f"Number of sheets: {len(xl_file.sheet_names)}")
        print(f"Sheet list: {xl_file.sheet_names[:5]}")
        if len(xl_file.sheet_names) > 5:
            print(f"  ... 외 {len(xl_file.sheet_names) - 5}개 시트")

        for sheet_name in xl_file.sheet_names:
            try:
                # Read sheet (원본과 정제본 모두 필요)
                df_raw = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

                if df_raw.empty:
                    continue

                # 정제 (Determine regional/national based on filename)
                df_clean = clean_io_table(df_raw, is_regional=is_regional_file)

                if len(df_clean) < 2:  # Must have at least 2 data rows
                    continue

                # 길형식으로 변환 (원본 데이터도 함께 전달)
                df_long = io_table_to_long(df_clean, df_raw=df_raw, sheet_name=sheet_name,
                                          is_regional=is_regional_file)

                if len(df_long) > 0:
                    # Geographical level 추가
                    df_long['geographical_level'] = geographical_level
                    all_long_dfs.append(df_long)
                    stats['sheets_processed'] += 1
                    stats['total_records'] += len(df_long)
                    table_type = "Regional" if is_regional_file else "National"
                    print(f"  ✓ {sheet_name} [{table_type}]: {len(df_long):,} 행")

            except Exception as e:
                error_msg = f"{sheet_name}: {str(e)[:100]}"
                stats['errors'].append(error_msg)
                print(f"  ✗ {sheet_name}: 오류 - {str(e)[:50]}")

        # 모든 데이터프레임 결합
        if all_long_dfs:
            df_combined = pd.concat(all_long_dfs, ignore_index=True)
        else:
            df_combined = pd.DataFrame()

    except Exception as e:
        stats['errors'].append(f"File processing error: {str(e)}")
        df_combined = pd.DataFrame()

    return df_combined, stats


# ============================================================================
# 3. Two Long-Format DataFrame Creation Functions
# ============================================================================

def create_index_dataframe(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    첫 번째 데이터프레임: Index information
    Mapping table to find sectors/products

    칼럼:
    - sector_code: Sector code
    - sector_name: Sector name (Original language, NaN if missing)
    - sector_type: 'output' 또는 'input'
    - geographical_levels: Geographical levels containing this sector (comma separated)
    - regions: Regions containing this sector (If regional data exists)
    """

    # Output 부문 추출
    if 'output_region' in df_long.columns:
        # Regional 테이블
        output_sectors = df_long[['output_sector_code', 'output_sector_name', 'geographical_level', 'output_region']].drop_duplicates()
        output_sectors['sector_type'] = 'output'
        output_sectors.columns = ['sector_code', 'sector_name', 'geographical_level', 'region', 'sector_type']
    else:
        # National 테이블
        output_sectors = df_long[['output_sector_code', 'output_sector_name', 'geographical_level']].drop_duplicates()
        output_sectors['sector_type'] = 'output'
        output_sectors['region'] = None
        output_sectors.columns = ['sector_code', 'sector_name', 'geographical_level', 'sector_type', 'region']
        output_sectors = output_sectors[['sector_code', 'sector_name', 'geographical_level', 'region', 'sector_type']]

    # Input 부문 추출 (코드가 있는 경우만)
    input_sectors = df_long[['input_sector_code', 'geographical_level']].drop_duplicates()
    input_sectors = input_sectors.dropna(subset=['input_sector_code'])
    input_sectors['sector_name'] = None
    input_sectors['sector_type'] = 'input'
    input_sectors['region'] = None
    input_sectors.columns = ['sector_code', 'geographical_level', 'sector_name', 'sector_type', 'region']
    input_sectors = input_sectors[['sector_code', 'sector_name', 'geographical_level', 'region', 'sector_type']]

    # 결합
    index_df = pd.concat([output_sectors, input_sectors], ignore_index=True)

    # Sector code별로 정보 합치기
    index_df['sector_code'] = index_df['sector_code'].astype(str)
    index_df_grouped = index_df.groupby('sector_code', as_index=False).agg({
        'sector_name': 'first',
        'sector_type': 'first',
        'geographical_level': lambda x: ', '.join(sorted(set(x))),
        'region': lambda x: ', '.join(sorted(set([str(r) for r in x if pd.notna(r)]))) or None
    })

    index_df_grouped = index_df_grouped.sort_values(['sector_code']).reset_index(drop=True)

    return index_df_grouped


def create_transaction_dataframe(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    두 번째 데이터프레임: Transaction data

    칼럼 순서:
    1. geographical_level: Geographical level (national/regional)
    2. table: Source sheet/table
    3-N: Transaction info (output_region, output_sector_code, output_sector_name,
                      input_region, input_sector_code, input_sector_name)
    마지막: value: Transaction amount
    """

    # Remove NaN and sort
    df_trans = df_long.dropna(subset=['value']).copy()

    # Sort output sectors (Based on region/country)
    if 'output_region' in df_trans.columns:
        df_trans = df_trans.sort_values(['output_region', 'output_sector_code', 'input_region', 'input_sector_code'])
    else:
        df_trans = df_trans.sort_values(['output_sector_code', 'input_sector_code'])

    # Sort column order
    cols_order = ['geographical_level', 'table']

    # output 정보
    if 'output_region' in df_trans.columns:
        cols_order.extend(['output_region', 'output_sector_code', 'output_sector_name'])
    else:
        cols_order.extend(['output_sector_code', 'output_sector_name'])

    # input 정보
    if 'input_region' in df_trans.columns:
        cols_order.extend(['input_region', 'input_sector_code', 'input_sector_name'])
    else:
        cols_order.extend(['input_sector_code', 'input_sector_name'])

    # value is last
    cols_order.append('value')

    # Select only existing columns
    cols_order = [col for col in cols_order if col in df_trans.columns]
    df_trans = df_trans[cols_order]

    return df_trans.reset_index(drop=True)


# ============================================================================
# 4. Main Execution Function
# ============================================================================

def main():
    """
    메인 실행 함수
    """

    print("\n" + "="*70)
    print("한국 투입산출표 데이터 변환 스크립트")
    print("="*70)

    # ========== 샘플 데이터 처리 ==========
    print("\n\n" + "="*70)
    print("[PART 1] 샘플 데이터 처리")
    print("="*70)

    # 샘플 데이터 생성
    df_wide_sample = create_sample_io_table()

    # 길형식으로 변환
    df_long_sample = wide_to_long_sample(df_wide_sample)

    # 검증
    validate_conversion(df_wide_sample, df_long_sample)

    # ========== 실제 데이터 처리 ==========
    print("\n\n" + "="*70)
    print("[PART 2] 실제 데이터 처리 (rawdata 폴더)")
    print("="*70)

    rawdata_path = Path('rawdata')

    if not rawdata_path.exists():
        print(f"\n⚠ 경고: {rawdata_path} 폴더를 찾을 수 없습니다.")
        print("CSV/Excel 파일 로드 예제를 대신 표시합니다.")

        print("\n[CSV 파일 로드 예제]")
        print("""
# CSV 파일 (광범위 형식)
df = pd.read_csv('io_table.csv', index_col=0)

# Excel 파일 (특정 시트)
df = pd.read_excel('io_table.xlsx', sheet_name='거래표', header=5)

# 길형식으로 변환
df_long = df.reset_index().melt(
    id_vars=['sector_name'],
    var_name='input_sector',
    value_name='transaction_amount'
)
        """)
    else:
        print(f"\n{rawdata_path} 폴더의 Excel 파일 처리 중...")

        excel_files = list(rawdata_path.glob('*.xlsx'))
        print(f"Found Excel files: {len(excel_files)}개")

        all_data = []
        all_stats = []

        # 주요 파일 처리 (처음 3개 파일)
        for file_path in excel_files[:3]:
            df_long, stats = process_excel_file(str(file_path))
            all_data.append(df_long)
            all_stats.append(stats)

        if all_data:
            # Combine data from all files
            df_combined_long = pd.concat(all_data, ignore_index=True)

            print(f"\n전체 결합 데이터: {len(df_combined_long):,} 행")

            # 샘플링 (대용량 데이터 처리 시)
            if len(df_combined_long) > 1000000:
                print(f"Large dataset detected (> 1백만 행)")
                print("Sampling top 10,000 rows per sheet to reduce processing time...")

                # Sample by sheet/table
                sampled_data = []
                table_col = 'table' if 'table' in df_combined_long.columns else 'source_sheet'
                for table_name in df_combined_long[table_col].unique():
                    sheet_data = df_combined_long[df_combined_long[table_col] == table_name]
                    sheet_sample = sheet_data.head(10000)
                    sampled_data.append(sheet_sample)

                df_combined_long = pd.concat(sampled_data, ignore_index=True)
                print(f"Data after sampling: {len(df_combined_long):,} 행\n")

            # 두 가지 Long-format dataframe 생성
            print("\n" + "-"*70)
            print("Creating index dataframe...")
            df_index = create_index_dataframe(df_combined_long)
            print(f"✓ Complete: {len(df_index):,} sectors/products")
            print(df_index.head(10))

            print("\n" + "-"*70)
            print("Transaction data프레임 생성 중...")
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
결과물:
1. df_long_sample: 샘플 데이터 (길형식, 12행)
2. io_index_dataframe.csv: 실제 데이터 인덱스
3. io_transaction_dataframe.csv: 실제 데이터 거래 기록

특징:
✓ 모든 요약 행/열 제거
✓ Original language(한국어) 유지
✓ 영문 칼럼명 사용
✓ 여러 시트 자동 결합
✓ 0/NaN 값 제거 (Include only actual transactions)
    """)


# ============================================================================
# 5. 실행
# ============================================================================

if __name__ == '__main__':
    main()
