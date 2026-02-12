# IO Table Converter - Project Structure

## 📁 Directory Layout

```
iotable/
├── main.py                          # 메인 스크립트 (함수 호출만)
│
├── libs/                            # 함수 라이브러리
│   ├── __init__.py
│   └── io_table_converter.py       # IO Table 변환 함수들
│
├── data/                            # 출력 데이터
│   ├── io_index_dataframe.csv
│   └── io_transaction_dataframe.csv
│
├── rawdata/                         # 입력 데이터 (원본 Excel 파일)
│   ├── 2020지역_투입산출표_...xlsx
│   ├── (표)(2020실측)투입산출표_...xlsx
│   └── ...
│
└── doc/                             # 문서
    ├── README_IO_CONVERTER.md       # 상세 설명서
    └── PROJECT_STRUCTURE.md         # 이 파일
```

## 🔧 주요 파일 설명

### `main.py` (메인 스크립트)
- **역할**: 함수 호출만 수행
- **구성**: 
  1. 샘플 데이터 생성 및 검증
  2. 실제 데이터 처리
  3. 결과 저장

```python
from libs.io_table_converter import (
    create_sample_io_table,
    wide_to_long_sample,
    validate_conversion,
    process_excel_file,
    create_index_dataframe,
    create_transaction_dataframe
)

def main():
    # 함수 호출
    ...
```

### `libs/io_table_converter.py` (함수 라이브러리)
- **역할**: 모든 함수 정의
- **포함된 함수**:
  - `create_sample_io_table()` - 샘플 데이터 생성
  - `wide_to_long_sample()` - 샘플 데이터 변환
  - `validate_conversion()` - 변환 검증
  - `identify_summary_rows()` - 요약 행 식별
  - `identify_summary_columns()` - 요약 열 식별
  - `clean_io_table()` - 데이터 정제
  - `is_regional_table()` - 지역/국가 테이블 판별 (폐기됨)
  - `io_table_to_long()` - 길형식 변환
  - `detect_geographical_level()` - 지역 수준 감지
  - `process_excel_file()` - Excel 파일 처리
  - `create_index_dataframe()` - 인덱스 생성
  - `create_transaction_dataframe()` - 거래 데이터 생성

## 🚀 실행 방법

### 기본 실행
```bash
python3 main.py
```

### 개별 함수 사용
```python
from libs.io_table_converter import create_sample_io_table

# 샘플 데이터 생성
df = create_sample_io_table()
```

## 📊 데이터 흐름

```
rawdata/*.xlsx
    ↓
[process_excel_file()]
    ↓
    ├─→ 정제 (clean_io_table)
    ├─→ 길형식 변환 (io_table_to_long)
    └─→ 지역 정보 추가
        ↓
    결합 (pd.concat)
        ↓
    샘플링 (10,000행/시트)
        ↓
    ├─→ [create_index_dataframe()]
    │       ↓
    │   data/io_index_dataframe.csv
    │
    └─→ [create_transaction_dataframe()]
            ↓
        data/io_transaction_dataframe.csv
```

## 📝 코드 분리 규칙

### main.py 에서 할 수 있는 것
✅ 함수 임포트  
✅ 함수 호출  
✅ 결과 출력  
✅ 간단한 제어 로직  

### main.py 에서 하면 안되는 것
❌ 함수 정의  
❌ 복잡한 비즈니스 로직  
❌ 데이터 처리 함수  

### libs/io_table_converter.py 에서 하는 것
✅ 모든 함수 정의  
✅ 복잡한 로직  
✅ 데이터 처리  

## 🔄 확장 방법

### 새로운 처리 함수 추가
1. `libs/io_table_converter.py`에 함수 정의
2. `main.py`에서 임포트
3. `main.py`의 `main()`에서 호출

### 새로운 분석 함수 추가
1. 새 파일 `libs/io_analyzer.py` 생성
2. 분석 함수 정의
3. `main.py`에서 임포트하여 사용

## 📚 문서 위치

- **README_IO_CONVERTER.md**: 상세 사용 설명서
- **PROJECT_STRUCTURE.md**: 프로젝트 구조 설명 (이 파일)

## ✅ 체크리스트

- ✓ 함수 라이브러리 분리 (`libs/`)
- ✓ 메인 스크립트 단순화 (`main.py`)
- ✓ 문서 통합 (`doc/`)
- ✓ 명확한 관심사 분리
- ✓ 재사용 가능한 구조

