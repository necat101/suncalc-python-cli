# SunCalc Python CLI

A Python CLI wrapper around the JavaScript [suncalc](https://github.com/mourner/suncalc) library for calculating sun and moon positions, rise/set times, and phases.

## Features

- Calculate sunrise, sunset, and all twilight phases for any location and date
- Get moonrise, moonset times, and lunar phase
- Support for coordinate input (lat/lng) or city name lookup via GeoPy
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
pip install geopy
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
Date: 2026-06-19 05:40:53 UTC

SUN TIMES
----------------------------------------------------------------------
  Night end            07:47:05 UTC
  Nautical dawn        08:33:56 UTC
  Dawn                 09:14:36 UTC
  Sunrise              09:46:49 UTC
  Sunrise end          09:50:02 UTC
  Golden hour end      10:26:54 UTC
  Solar noon           17:14:19 UTC
  Golden hour          00:01:45 UTC
  Sunset start         00:38:38 UTC
  Sunset               00:41:51 UTC
  Dusk                 01:14:04 UTC
  Nautical dusk        01:54:44 UTC
  Night                02:41:37 UTC

Sun position: altitude -26.70°, azimuth 6.88°

MOON TIMES
----------------------------------------------------------------------
  Moonrise: 14:53:07 UTC
  Moonset:  03:55:42 UTC

Moon phase: Waxing Crescent
  Illumination: 22.8%
  Phase value: 0.158
  Waxing: True

Moon position: altitude -18.16°, azimuth 305.63°
Distance: 372340 km
======================================================================
```

## How It Works

1. **Python CLI** (`suncalc_cli.py`) - Handles argument parsing, geocoding via GeoPy, and output formatting
2. **Node.js Bridge** (`suncalc_bridge.js`) - Interfaces with the suncalc JavaScript library
3. **suncalc.js** - Performs the actual astronomical calculations (installed via npm)

The Python script calls the Node.js bridge via subprocess, passing JSON input and receiving JSON output.

## Requirements

- Python 3.6+
- Node.js 12+
- geopy (Python package)
- suncalc (npm package)

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
