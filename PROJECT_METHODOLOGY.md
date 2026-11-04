# Project Methodology

## Objective and source boundary
Explore the six supplied PhonePe Pulse CSV files only. No external datasets, APIs or enrichment are used.

## Consolidation
Append the six CSVs vertically into data/processed/phonepe_pulse_master.csv. This is a union/append, not a side-by-side join. The master contains 51,442 rows and 13 standardised columns. source_dataset identifies the original source; source_row_id preserves the export row identifier. Non-applicable dimensions and measures remain blank.

## Source grains
- aggregated_transaction: state × year × quarter × transaction type
- aggregated_user: state × year × quarter × device brand
- map_transaction: state × year × quarter × district
- map_user: state × year × quarter × district
- top_transaction: state × year × quarter × district ranking extract
- top_user: state × year × quarter × district ranking extract

## Dashboard safeguards
- Transaction KPIs and category trends use aggregated_transaction.
- District transaction analysis uses map_transaction.
- Registered-user snapshots use map_user at the latest selected period.
- Device analysis uses aggregated_user.
- Top-list extracts are rankings only; never add them to map or aggregate totals.

## Limitations
Transaction value is payment value, not PhonePe corporate revenue. Registered-user counts are snapshots. Supplied data covers 2018–2022. No coordinates or boundary geometries are supplied, so the geographic visual is a treemap, not a choropleth.
