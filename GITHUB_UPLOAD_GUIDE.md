# Publish the revised project on GitHub

## Update your existing repository with GitHub Desktop

1. Open GitHub Desktop and select `phonepe-pulse-analytics`.
2. Choose **Repository → Show in Finder**.
3. Copy the contents of this extracted `phonepe_pulse_project_revised` folder into the repository folder, replacing files when asked.
4. Confirm that `data/processed/phonepe_pulse_master.csv` is included and all six original files remain in `data/source/`.
5. Review the changed files in GitHub Desktop.
6. Commit with the message `Consolidate six PhonePe datasets and update dashboard`.
7. Click **Push origin**.

Before making the repository public, confirm that you have permission to redistribute the supplied CSV data. A public repository makes all committed data downloadable by anyone.

## Run after cloning
Open the repository folder and double-click `START_DASHBOARD.command`. The first run needs an internet connection to install free Python packages.
