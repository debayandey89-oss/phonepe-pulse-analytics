# PhonePe Pulse Analytics Dashboard

A Streamlit dashboard built using only the six supplied PhonePe Pulse CSV files (2018–2022). The files are vertically appended into one consolidated master CSV; no external data, APIs or enrichment are used.

## Run on macOS
1. Download and extract the project ZIP.
2. Open the project folder and double-click START_DASHBOARD.command.
3. Keep Terminal open while the dashboard runs.
4. If the browser does not open, visit http://localhost:8501.
5. Stop with Control + C in Terminal.

## Data architecture
The dashboard reads data/processed/phonepe_pulse_master.csv: 51,442 rows, 13 standardised columns and six source sections. This is an append/union, not a side-by-side join. source_dataset identifies the original source of every row. Blank dimensions and measures are intentional when not applicable.

The six untouched source CSVs remain in data/source/ for traceability.

## Dashboard
- Executive overview and transaction KPIs
- Quarterly transaction trends and category mix
- State and district transaction analysis
- Registered-user and device-brand analysis
- Top-user and top-transaction rankings
- Data-quality and methodology notes
- Download of the consolidated master CSV

## Interpretation safeguards
- Transaction value is not PhonePe corporate revenue.
- Aggregated and district transaction datasets have different grains; never add them together.
- Registered-user counts are snapshots, not cumulative quarterly flows.
- Top-list extracts are rankings, not additive totals.
- Data covers 2018–2022 only.
- No coordinates or boundary polygons are supplied; the dashboard uses a treemap, not a choropleth.

## Key files
app.py; data/processed/phonepe_pulse_master.csv; data/source/; DATA_DICTIONARY.md; PROJECT_METHODOLOGY.md; DATA_VALIDATION_REPORT.json; START_DASHBOARD.command.
