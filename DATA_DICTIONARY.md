# Data Dictionary

## Consolidated master file

`data/processed/phonepe_pulse_master.csv` contains **51,442 rows** appended from the six supplied CSVs. It is a vertical union (append), not a side-by-side join. Every row carries `source_dataset`, which identifies its original source and preserves its analytical grain.

| Column | Meaning |
|---|---|
| source_dataset | One of the six original dataset identifiers |
| source_row_id | Original export index / row identifier from the source |
| state | State or union territory |
| year, quarter | Reporting period |
| district | District, where supplied |
| transaction_type | Transaction category, where supplied |
| device_brand | Device brand, where supplied |
| transaction_count | Transaction count, where supplied |
| transaction_amount | Transaction amount, where supplied |
| registered_user_count | Registered-user count, where supplied |
| device_user_count | Device-user count, where supplied |
| percentage | Brand percentage, where supplied |

Blank values are intentional when a dimension or measure does not apply to a source dataset.

## Source sections and grains

| source_dataset | Rows | Dimensions | Measures |
|---|---:|---|---|
| aggregated_transaction | 3,594 | state, year, quarter, transaction_type | transaction_count, transaction_amount |
| aggregated_user | 6,732 | state, year, quarter, device_brand | device_user_count, percentage |
| map_transaction | 14,636 | state, year, quarter, district | transaction_count, transaction_amount |
| map_user | 14,640 | state, year, quarter, district | registered_user_count |
| top_transaction | 5,920 | state, year, quarter, district | transaction_count, transaction_amount |
| top_user | 5,920 | state, year, quarter, district | registered_user_count |

The six untouched source files remain in `data/source/` for traceability. The dashboard loads the consolidated master and filters by `source_dataset` before performing analysis.
