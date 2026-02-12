# 한국 투입산출표(IO Table) 데이터 변환 스크립트

## 개요
이 스크립트는 한국의 투입산출표(Input-Output Table) 데이터를 처리하여 광범위(wide-format) 데이터를 길형식(long-format) 데이터로 변환합니다.

## 특징

✅ **자동 데이터 정제**
- 모든 요약 행 자동 제거 (중간투입계, 부가가치계, 총투입계 등)
- 모든 요약 열 자동 제거 (합계, 총계 등)
- 0 값 및 NaN 값 자동 제거

✅ **다중 시트 처리**
- Excel 파일의 모든 시트 자동 처리
- 여러 파일의 데이터 자동 결합
- 각 시트의 출처 정보 추적

✅ **언어 유지**
- 원본 데이터의 한국어 유지 (번역 없음)
- 칼럼명은 영어로 표준화

✅ **두 가지 길형식 데이터프레임 생성**
1. **인덱스 데이터프레임**: 모든 섹터/상품 목록
2. **거래 데이터프레임**: 모든 거래 기록 (생산부문 → 투입부문)

---

## 결과 파일

### 1. `io_index_dataframe.csv`
섹터/상품 인덱싱 테이블

**칼럼:**
| 칼럼명 | 설명 | 예시 |
|--------|------|------|
| `sector_code` | 섹터 코드 | `0111`, `1000` |
| `sector_name` | 섹터/상품명 (한국어) | `벼`, `담배` |
| `sector_type` | 부문 유형 | `output` 또는 `input` |

**용도:**
- 섹터 코드와 이름 매핑
- 상품 분류 체계 확인

---

### 2. `io_transaction_dataframe.csv`
거래 기록 데이터프레임

**칼럼:**
| 칼럼명 | 설명 | 예시 |
|--------|------|------|
| `output_sector_code` | 생산 부문 코드 | `0111` |
| `output_sector_name` | 생산 부문명 (한국어) | `벼` |
| `input_sector_code` | 투입 부문 코드 | `1000` |
| `transaction_amount` | 거래액 (백만원) | `137663.0` |
| `source_sheet` | 출처 시트 | `A표_총거래표(생산자)` |

**구조:**
```
생산부문 ----거래액----> 투입부문
(output)              (input)
```

---

## 사용 예시

### Python에서 로드
```python
import pandas as pd

# 인덱스 데이터프레임 로드
df_index = pd.read_csv('io_index_dataframe.csv', encoding='utf-8-sig')

# 거래 데이터프레임 로드
df_transaction = pd.read_csv('io_transaction_dataframe.csv', encoding='utf-8-sig')

# 특정 상품의 거래 조회
rice_transactions = df_transaction[
    df_transaction['output_sector_name'] == '벼'
]
print(rice_transactions)

# 상품명으로 코드 검색
sector_code = df_index[df_index['sector_name'] == '담배']['sector_code'].values[0]
print(f"담배의 코드: {sector_code}")
```

### 데이터 분석
```python
# 상위 10개 거래액
top_transactions = df_transaction.nlargest(10, 'transaction_amount')

# 생산부문별 총 거래액
output_totals = df_transaction.groupby('output_sector_name')['transaction_amount'].sum()

# 투입부문별 총 거래액
input_totals = df_transaction.groupby('input_sector_code')['transaction_amount'].sum()
```

---

## 데이터 검증

### 샘플 데이터 검증 결과
✓ 행 합계 일치 (광범위 ↔ 길형식)
✓ 열 합계 일치 (광범위 ↔ 길형식)
✓ 총 거래액 일치

```
샘플 데이터:
광범위 형식 총합: 226,280 백만원
길형식 총합:     226,280 백만원
```

---

## 실제 데이터 처리

### 처리된 파일
1. `2020지역_투입산출표_생산자가격_통합소분류_생산유발계수.xlsx`
   - 생산유발계수 시트: 6,716,193 행 → 샘플링 후 10,000 행

2. `(표)(2020실측)투입산출표_생산자가격_기본부문.xlsx`
   - 12개 시트 처리
   - A표_총거래표(생산자): 80,783 행 → 샘플링 후 10,000 행
   - A표_수입거래표(생산자): 30,946 행 → 샘플링 후 10,000 행
   - A표_국산거래표(생산자): 77,790 행 → 샘플링 후 10,000 행
   - 기타 계수 시트들...

3. `2020지역_투입산출표_생산자가격_통합소분류_부가가치유발계수.xlsx`
   - 부가가치유발계수: 6,596,093 행 → 샘플링 후 10,000 행

### 결과 통계
- 전체 결합 데이터: 14,045,191 행
- 샘플링 후: 90,000 행 (각 시트별 상위 10,000행)
- 생성된 인덱스: 2,877개 섹터/상품
- 생성된 거래 기록: 90,000개

---

## 스크립트 구조

### 1. 샘플 데이터 처리 (PART 1)
```python
# 샘플 데이터 생성 (4x4 매트릭스)
df_wide_sample = create_sample_io_table()

# 길형식 변환
df_long_sample = wide_to_long_sample(df_wide_sample)

# 검증
validate_conversion(df_wide_sample, df_long_sample)
```

### 2. 실제 데이터 처리 (PART 2)
```python
# rawdata 폴더의 모든 Excel 파일 처리
for file_path in excel_files:
    df_long, stats = process_excel_file(str(file_path))

# 모든 시트 데이터 결합
df_combined = pd.concat(all_long_dfs, ignore_index=True)

# 두 가지 길형식 데이터프레임 생성
df_index = create_index_dataframe(df_combined)
df_transaction = create_transaction_dataframe(df_combined)

# CSV로 저장
df_index.to_csv('io_index_dataframe.csv', ...)
df_transaction.to_csv('io_transaction_dataframe.csv', ...)
```

---

## 주요 함수 설명

### `clean_io_table()`
- 헤더 행 제거 (처음 5행)
- 요약 행 식별 및 제거
- 요약 열 식별 및 제거
- NaN 행 제거

### `io_table_to_long()`
- 광범위 형식을 길형식으로 변환
- melt() 함수 사용
- 거래액 숫자 변환
- 0값 및 NaN 제거

### `create_index_dataframe()`
- Output 부문 추출
- Input 부문 추출
- 중복 제거 및 정렬

### `create_transaction_dataframe()`
- NaN 값 제거
- 정렬 (output → input 순서)
- 인덱스 리셋

---

## 성능 고려사항

### 대용량 데이터 샘플링
- 1백만 행 이상의 데이터는 자동으로 샘플링됨
- 각 시트별로 상위 10,000행만 처리
- 전체 데이터 탐색용으로 충분

### 메모리 사용
- 샘플링 전: ~14백만 행
- 샘플링 후: ~90,000 행
- CSV 파일 크기: ~36KB (인덱스) + ~5.4MB (거래)

---

## 사용 방법

### 1. 스크립트 실행
```bash
python3 io_table_converter.py
```

### 2. 출력 확인
```bash
# 생성된 파일 확인
ls -lh io_*.csv

# 내용 확인
head io_index_dataframe.csv
head io_transaction_dataframe.csv
```

### 3. 데이터 분석
```python
import pandas as pd
df = pd.read_csv('io_transaction_dataframe.csv', encoding='utf-8-sig')
print(df.shape)
print(df.dtypes)
print(df.head())
```

---

## 주의사항

1. **원본 데이터 유지**: rawdata 폴더의 원본 Excel 파일은 수정되지 않음
2. **인코딩**: CSV 파일은 UTF-8-BOM 인코딩 사용 (한글 표시 최적화)
3. **대용량 데이터**: 샘플링으로 인해 전체 데이터의 일부만 포함
4. **입력 부문 이름 없음**: input_sector_code만 있고 이름 정보는 없음 (원본 데이터 구조상)

---

## 문제 해결

### CSV 파일이 한글로 깨져서 보일 때
```python
# UTF-8-BOM 인코딩으로 명시적으로 로드
df = pd.read_csv('io_transaction_dataframe.csv', encoding='utf-8-sig')
```

### 대용량 파일 전체 처리
스크립트에서 아래 줄을 수정:
```python
if len(df_combined_long) > 1000000000:  # 10억 행 이상일 때만 샘플링
```

---

## 라이선스 및 참고
- 원본 데이터: 한국은행 통계청
- 스크립트 언어: Python 3.8+
- 주요 라이브러리: pandas, numpy, openpyxl
