# Data Dictionary

| File | Rows in supplied source | Dimensions | Measures |
|---|---:|---|---|
| aggregated_transaction.csv | 3,594 | states, year, quarter, trans_type | trans_counts, amount |
| aggregated_user.csv | 6,732 | states, year, quarter, brand | user_counts, percentage |
| map_transaction.csv | 14,636 | states, year, quarter, district | trans_counts, amount |
| map_user.csv | 14,640 | states, year, quarter, district | registered_user_counts |
| top_transaction.csv | 5,920 | states, year, quarter, district | trans_counts, amount |
| top_user.csv | 5,920 | states, year, quarter, district | registered_user_counts |

All six files cover 2018–2022 and quarters 1–4 in the supplied copy. `Unnamed: 0` is an export index and is removed from the processed copies. State and district names are title-cased and normalised for display. The original files remain unchanged in `data/source/`.
