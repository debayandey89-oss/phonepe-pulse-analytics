# Project Methodology

## Objective
Explore the six supplied PhonePe Pulse CSV files to analyse transaction value, transaction count, registered-user distribution, device-brand composition and state/district patterns.

## Source boundary
Only these files are used: aggregated_transaction, aggregated_user, map_transaction, map_user, top_transaction and top_user. No outside data is fetched or joined.

## Preparation
1. Retain an untouched copy of each source CSV in `data/source/`.
2. Remove export index columns named `Unnamed: ...`.
3. Standardise state and district labels for consistent display.
4. Preserve all supplied measures and dimensions.
5. Store normalised copies in `data/processed/`.

## Data grains
- Aggregated transactions: state × year × quarter × transaction type.
- Aggregated users: state × year × quarter × device brand.
- Map transactions: state × year × quarter × district.
- Map users: state × year × quarter × district.
- Top transactions: state × year × quarter × district ranking extract.
- Top users: state × year × quarter × district ranking extract.

## KPI definitions
- Transaction value: sum of `amount` for selected aggregated transaction records.
- Transaction count: sum of `trans_counts` for selected aggregated transaction records.
- Average transaction value: transaction value divided by transaction count.
- Registered users: sum of district `registered_user_counts` in the latest selected year-quarter snapshot.
- Device users: sum of `user_counts` in the selected aggregated-user brand data; interpret according to the supplied source measure.
- YoY: current quarter divided by the same quarter in the prior year, minus one.
- QoQ: current quarter divided by the immediately preceding quarter, minus one.

## Limitations
The supplied CSVs have state and district labels but no coordinates or polygon geometries. A true boundary map would require external geography data, which is intentionally excluded. The dashboard therefore uses an interactive hierarchical treemap. Data is limited to 2018–2022 as supplied. The data does not report PhonePe's corporate revenue.
