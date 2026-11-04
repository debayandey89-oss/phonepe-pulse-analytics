# PhonePe Pulse Analytics Dashboard

A Streamlit dashboard built using **only the six supplied PhonePe Pulse CSV files** (2018–2022). The six files are appended into one consolidated master CSV; no outside data, APIs or enrichment are used.

## Run it on a Mac

1. Download and extract the project ZIP.
2. Open the `phonepe_pulse_project` folder.
3. Double-click `START_DASHBOARD.command`.
4. The first run may take a few minutes while free Python packages install. Keep Terminal open.
5. If the browser does not open, visit http://localhost:8501.
6. Stop the dashboard with Control + C in Terminal.

If macOS blocks the command file, Control-click it, choose Open, and confirm. If Python 3 is missing, install it from https://www.python.org/downloads/macos/.

## Data architecture

`data/processed/phonepe_pulse_master.csv` is the single data file used by the dashboard. It contains 51,442 rows appended from six source files, with a common schema and a `source_dataset` column identifying each row's origin.

This is a vertical append/union, **not a side-by-side join**. Blank fields are intentional where a measure or dimension does not apply to a particular source. The six untouched originals are retained in `data/source/`.

## Dashboard contents
- Executive overview and transaction KPIs
- Quarterly transaction trends, category mix and growth
- State and district transaction analysis
- Registered-user and device-brand analysis
- Top-user and top-transaction rankings
- Data quality, source inventory and methodology
- Download of the consolidated master CSV

## Interpretation safeguards
- Transaction value is not PhonePe's corporate revenue.
- Aggregated and district map transaction datasets are different grains; do not add them together.
- Registered-user counts are snapshots, not flows; do not sum across quarters as cumulative users.
- Top-user and top-transaction files are ranking extracts, not additional totals to add to map data.
- The supplied data spans 2018–2022 only.
- The CSVs contain no coordinates or boundary polygons, so the dashboard uses a treemap rather than a true choropleth.

## Project structure
- `app.py` — dashboard
- `data/processed/phonepe_pulse_master.csv` — consolidated master used by dashboard
- `data/source/` — six original CSVs
- `START_DASHBOARD.command` — Mac launcher
- `requirements.txt` — dependencies
- `DATA_DICTIONARY.md` — master schema and source grains
- `PROJECT_METHODOLOGY.md` — consolidation and analytical rules
- `DATA_VALIDATION_REPORT.json` — validation checks
- `INSIGHTS_TEMPLATE.md` — findings template
- `GITHUB_UPLOAD_GUIDE.md` — publishing guide
