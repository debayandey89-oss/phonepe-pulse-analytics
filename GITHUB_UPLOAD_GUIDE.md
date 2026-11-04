# Publish this project on GitHub

The repository already contains the dashboard code and project documentation. To add the six CSV datasets from the project folder on your Mac, use GitHub Desktop.

## Add the local project files to the existing repository
1. Install GitHub Desktop from https://desktop.github.com/ and sign in.
2. In GitHub Desktop choose **File → Clone Repository**.
3. Select `debayandey89-oss/phonepe-pulse-analytics` and clone it to your Mac.
4. Open the downloaded/extracted `phonepe_pulse_project` folder from the project ZIP in Finder.
5. Copy the contents of that folder into the cloned `phonepe-pulse-analytics` folder. Choose **Replace** for matching files when macOS asks. This copies the six source and processed CSVs as well.
6. Return to GitHub Desktop. Review the changed files, enter the summary `Add supplied PhonePe Pulse datasets and project files`, and click **Commit to main**.
7. Click **Push origin**.

## Public data warning
This repository is public. The six supplied CSVs will be visible to anyone after you push them. Confirm that you have permission to redistribute the data before publishing. If not, keep the repository private and share access only with evaluators.

## Running the dashboard
After cloning the complete repository, double-click `START_DASHBOARD.command` on macOS. The first run needs an internet connection to install free Python packages. Keep the Terminal window open while the dashboard runs.
