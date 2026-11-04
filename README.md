# PhonePe Pulse Analytics Dashboard

An interactive Streamlit dashboard built using **only the six CSV files supplied for this project**. The supplied data covers 2018–2022. No outside dataset or API is used.

> **Dataset upload still required:** The repository currently contains the dashboard and documentation. The six CSVs are in the downloadable project ZIP but have not yet been committed to this GitHub repository. Before running the app from this repository, follow [GITHUB_UPLOAD_GUIDE.md](GITHUB_UPLOAD_GUIDE.md) to copy the supplied project files and commit them.

## Run locally on macOS

1. Complete the dataset upload described above (or use the complete project ZIP locally).
2. Open the project folder.
3. Double-click `START_DASHBOARD.command`.
4. Keep the Terminal window open while the dashboard runs. On first launch it installs the free Python dependencies.
5. Visit http://localhost:8501 if the browser does not open automatically.
6. Press Control+C in Terminal to stop the dashboard.

If macOS blocks the launcher, Control-click it, choose Open, and confirm. Python 3 is required; install it from https://www.python.org/downloads/macos/ if needed.

## Dashboard features

- Executive overview and transaction KPIs
- Quarterly transaction trends and transaction-category mix
- Year-on-year and quarter-on-quarter comparisons
- State and district rankings
- Registered-user and device-brand analysis
- Interactive state/district treemap
- Data-quality and methodology notes

## Data safeguards

- Only the six supplied CSVs are used; no external dataset, API, or geography enrichment is used.
- Transaction value is not PhonePe's corporate revenue.
- Aggregated transaction and district map data have different grains and must not be added together.
- Registered-user counts are snapshots, not quarterly flows.
- Top-user and top-transaction files are ranking extracts, not additional totals.
- The supplied data spans 2018–2022 only.
- The CSVs contain names and measures, not coordinates or boundary polygons. A true choropleth would require external geography data, so this project uses a treemap.

## Project structure

- `app.py` — Streamlit dashboard
- `START_DASHBOARD.command` — macOS launcher
- `requirements.txt` — Python dependencies
- `data/source/` — original supplied CSVs
- `data/processed/` — cleaned copies used by the dashboard
- `PROJECT_METHODOLOGY.md` — methods and KPI definitions
- `DATA_DICTIONARY.md` — schemas and grains
- `DATA_VALIDATION_REPORT.json` — validation summary
- `INSIGHTS_TEMPLATE.md` — evidence-led findings template

See the methodology and validation report before interpreting results.
