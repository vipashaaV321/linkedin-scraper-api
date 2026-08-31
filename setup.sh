#!/usr/bin/env bash
set -euo pipefail

echo "Setting up linkedin_scraper_api..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete. To run the demo:" 
echo "  PYTHONPATH=. python3 linkedin_scraper_api/scripts/main.py williamhgates"
