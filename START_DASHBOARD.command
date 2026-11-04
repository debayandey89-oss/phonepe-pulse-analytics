#!/bin/bash
set -e
cd "$(dirname "$0")"

clear
printf '\n===========================================\n'
printf '       PHONEPE PULSE DASHBOARD\n'
printf '===========================================\n\n'

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 was not found."
  echo "Please install Python 3 from https://www.python.org/downloads/macos/"
  echo "Then double-click this file again."
  read -r -p "Press Return to close..."
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "First-time setup: creating a private Python environment..."
  python3 -m venv .venv
fi

echo "Preparing dashboard dependencies (first run may take a few minutes)..."
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

echo "\nStarting the dashboard..."
echo "Keep this Terminal window open while using the dashboard."
echo "Your browser should open automatically. If not, visit http://localhost:8501"
echo "To stop the dashboard, return here and press Control + C."
echo ""
.venv/bin/python -m streamlit run app.py
