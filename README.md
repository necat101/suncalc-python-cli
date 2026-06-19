# SunCalc Python CLI

A Python CLI wrapper around the JavaScript [suncalc](https://github.com/mourner/suncalc) library for calculating sun and moon positions, rise/set times, and phases.

## Features

- Calculate sunrise, sunset, and all twilight phases for any location and date
- Get moonrise, moonset times, and lunar phase
- Support for coordinate input (lat/lng) or city name lookup via GeoPy
- **Automatic local timezone detection and display** - times shown in local timezone
- Output in human-readable format or JSON
- Uses the accurate suncalc.js library (v2.0) - matches US Naval Observatory data

## Installation

```bash
# Clone the repository
git clone https://github.com/necat101/suncalc-python-cli.git
cd suncalc-python-cli

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install geopy timezonefinder
```

## Usage

### With coordinates:
```bash
python3 suncalc_cli.py --lat 51.5 --lng -0.1 --date 2026-08-24
```

### With city name:
```bash
python3 suncalc_cli.py --city "London, UK" --date 2026-08-24
python3 suncalc_cli.py --city "New York"
python3 suncalc_cli.py --city "Stephens City, VA"
python3 suncalc_cli.py --city "Tokyo, Japan" --date "2026-06-21T12:00:00Z"
```

### JSON output:
```bash
python3 suncalc_cli.py --lat 40.7128 --lng -74.0060 --json
```

### Options:
- `--lat LAT`: Latitude in decimal degrees
- `--lng LNG`: Longitude in decimal degrees  
- `--city CITY`: City name (e.g., 'London' or 'London, UK') - requires geopy
- `--date DATE`: Date/time in ISO format (default: now)
- `--json`: Output raw JSON instead of formatted text
- `--no-moon`: Skip moon calculations

## Example Output

```
======================================================================
SunCalc Results
======================================================================
Location: Stephens City, Frederick County, Virginia, United States
Coordinates: 39.083222°N, -78.218285°E
Timezone: America/New_York
Date: 2026-06-19 01:44:50 EDT

SUN TIMES
----------------------------------------------------------------------
  Night end            03:47:05 EDT
  Nautical dawn        04:33:56 EDT
  Dawn                 05:14:36 EDT
  Sunrise              05:46:49 EDT
  Sunrise end          05:50:02 EDT
  Golden hour end      06:26:54 EDT
  Solar noon           13:14:19 EDT
  Golden hour          20:01:45 EDT
  Sunset start         20:38:38 EDT
  Sunset               20:41:51 EDT
  Dusk                 21:14:04 EDT
  Nautical dusk        21:54:44 EDT
  Night                22:41:37 EDT

Sun position: altitude -26.60°, azimuth 7.89°

MOON TIMES
----------------------------------------------------------------------
  Moonrise: 10:53:07 EDT
  Moonset:  23:55:42 EDT

Moon phase: Waxing Crescent
  Illumination: 22.8%
  Phase value: 0.158
  Waxing: True

Moon position: altitude -18.77°, azimuth 306.37°
Distance: 372356 km
======================================================================
```

**Note:** Times are automatically displayed in the local timezone of the location (EDT for Stephens City, VA, BST for London, JST for Tokyo, etc.)

## How It Works

1. **Python CLI** (`suncalc_cli.py`) - Handles argument parsing, geocoding via GeoPy, timezone lookup, and output formatting
2. **Node.js Bridge** (`suncalc_bridge.js`) - Interfaces with the suncalc JavaScript library
3. **suncalc.js** - Performs the actual astronomical calculations (installed via npm)

The Python script calls the Node.js bridge via subprocess, passing JSON input and receiving JSON output. Times are converted from UTC to local timezone using `timezonefinder` and Python's `zoneinfo`.

## Requirements

- Python 3.9+ (for zoneinfo)
- Node.js 12+
- geopy (Python package) - for city geocoding
- timezonefinder (Python package) - for timezone lookup
- suncalc (npm package) - for astronomical calculations

## Accuracy

Calculations match [timeanddate.com](https://www.timeanddate.com/) and the [U.S. Naval Observatory](https://aa.usno.navy.mil/). Based on Jean Meeus' Astronomical Algorithms.

Typical errors:
- Sun position: ~0.08°
- Rise/set times: ~15 seconds
- Moon position: ~0.09°
- Moon distance: ~20 km

## License

This wrapper is provided as-is. The underlying suncalc library is [ISC Licensed](https://github.com/mourner/suncalc/blob/master/LICENSE).

## Credits

- [SunCalc](https://github.com/mourner/suncalc) by Vladimir Agafonkin
- Built for use with OpenClaw
