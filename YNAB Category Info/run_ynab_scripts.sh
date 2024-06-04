#!/bin/bash
# Make sure to change the paths to where you have this folder if you use this script.
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
    python ynab_category_spending_check.py
    python ynab_category_balances.py
else
    source .venv/bin/activate
    python ynab_category_spending_check.py
    python ynab_category_balances.py

fi
deactivate