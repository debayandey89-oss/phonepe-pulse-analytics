# Data Dictionary

## Consolidated master
data/processed/phonepe_pulse_master.csv contains 51,442 rows appended from the six source CSVs. It is a vertical union, not a side-by-side join. Every row has source_dataset and source_row_id.

| Column | Meaning |
|---|---|
| source_dataset | Original source identifier |
| source_row_id | Original source export row identifier |
| state | State / union territory |
| year, quarter | Reporting period |
| district | District, when supplied |
| transaction_type | Transaction category, when supplied |
| device_brand | Device brand, when supplied |
| transaction_count | Transaction count, when supplied |
| transaction_amount | Transaction amount, when supplied |
| registered_user_count | Registered-user count, when supplied |
| device_user_count | Device-user count, when supplied |
| percentage | Brand percentage, when supplied |

Blank values are intentional where a field does not apply.

## Source grains and row counts
| source_dataset | Rows | Grain |
|---|---:|---|
| aggregated_transaction | 3,594 | state × year × quarter × transaction type |
| aggregated_user | 6,732 | state × year × quarter × device brand |
| map_transaction | 14,636 | state × year × quarter × district |
| map_user | 14,640 | state × year × quarter × district |
| top_transaction | 5,920 | state × year × quarter × district ranking extract |
| top_user | 5,920 | state × year × quarter × district ranking extract |

Original source CSVs are retained in data/source/. Dashboard analyses first filter by source_dataset to preserve each source's grain.
