# Project Methodology

## Objective
Build a reproducible PhonePe Pulse analytics dashboard using exactly the six supplied CSV files, with no external datasets, APIs or enrichment.

## Consolidation design
The six CSVs are appended vertically into `data/processed/phonepe_pulse_master.csv`. This is a union/append operation, **not** a side-by-side join. The master has 51,442 rows and a standardised 13-column schema. `source_dataset` records which source each row came from; non-applicable dimensions and measures remain blank. `source_row_id` preserves the source export row identifier.

## Source grains
- `aggregated_transaction`: state × year × quarter × transaction type.
- `aggregated_user`: state × year × quarter × device brand.
- `map_transaction`: state × year × quarter × district.
- `map_user`: state × year × quarter × district.
- `top_transaction`: state × year × quarter × district top-list extract.
- `top_user`: state × year × quarter × district top-list extract.

## Dashboard modelling safeguards
The dashboard reads the one master CSV, then separates its six source sections using `source_dataset`. It does not combine overlapping measures across grains.
- Transaction KPIs and category trends use `aggregated_transaction`.
- District transaction analysis uses `map_transaction`.
- Registered-user snapshots use `map_user` at the latest selected year-quarter.
- Device analysis uses `aggregated_user`.
- Top-list extracts are used only for rankings, never added to map or aggregate totals.

## KPI definitions
- Transaction value: sum of `transaction_amount` from selected aggregated transaction records.
- Transaction count: sum of `transaction_count` from selected aggregated transaction records.
- Average transaction value: transaction value divided by transaction count.
- Registered users: sum of district registered-user counts in the latest selected year-quarter snapshot.
- Device users: supplied device-user count from aggregated user data; interpret according to the source measure.
- YoY: current quarter divided by the same quarter in the prior year, minus one.
- QoQ: current quarter divided by the immediately preceding quarter, minus one.

## Limitations
The supplied CSVs contain state and district labels but no coordinates or polygon geometries. A true geographic boundary map would require external geography data, which is excluded. The dashboard therefore uses a hierarchical treemap. The supplied data spans 2018–2022. Transaction value is not PhonePe corporate revenue.
