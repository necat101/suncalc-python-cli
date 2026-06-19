#!/bin/bash
# Demo script for suncalc-python

echo "=== SunCalc Python CLI Demo ==="
echo

echo "1. London with coordinates:"
echo "   python3 suncalc_cli.py --lat 51.5 --lng -0.1 --date 2026-08-24"
echo
python3 suncalc_cli.py --lat 51.5 --lng -0.1 --date 2026-08-24 2>/dev/null | grep -A 5 "SunCalc Results"
echo

echo "2. Stephens City, VA (your hometown):"
echo "   python3 suncalc_cli.py --city 'Stephens City, VA'"
echo
python3 suncalc_cli.py --city "Stephens City, VA" 2>&1 | grep -E "(Location:|Coordinates:|Sunrise|Sunset|Solar noon|Moon phase)" | head -6
echo

echo "3. JSON output for Tokyo:"
echo "   python3 suncalc_cli.py --city 'Tokyo' --json"
echo
python3 suncalc_cli.py --city "Tokyo" --date 2026-06-21 --json 2>/dev/null | python3 -c "import json, sys; d=json.load(sys.stdin); print('Sunrise:', d['sun']['times']['sunrise']); print('Sunset:', d['sun']['times']['sunset'])"
echo

echo "Demo complete! See README.md for full documentation."
