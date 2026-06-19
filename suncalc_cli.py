#!/usr/bin/env python3
"""
SunCalc CLI - Calculate sun and moon rise/set times using the JavaScript suncalc library

Usage:
    python suncalc_cli.py --lat 51.5 --lng -0.1 --date 2026-08-24
    python suncalc_cli.py --city "London, UK" --date 2026-08-24
    python suncalc_cli.py --lat 40.7128 --lng -74.0060
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

try:
    from geopy.geocoders import Nominatim
    from geopy.exc import GeopyError
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False
    print("Warning: geopy not installed. City lookup disabled.", file=sys.stderr)
    print("Install with: pip install geopy", file=sys.stderr)

try:
    from timezonefinder import TimezoneFinder
    TZ_FINDER = TimezoneFinder()
    TZ_AVAILABLE = True
except ImportError:
    TZ_AVAILABLE = False
    TZ_FINDER = None
    print("Warning: timezonefinder not installed. Times will be shown in UTC.", file=sys.stderr)
    print("Install with: pip install timezonefinder", file=sys.stderr)


def geocode_location(location_string):
    """Convert city/country to coordinates using GeoPy/Nominatim"""
    if not GEOPY_AVAILABLE:
        raise RuntimeError("geopy is required for city lookup. Install with: pip install geopy")
    
    geolocator = Nominatim(user_agent="suncalc-cli/1.0")
    try:
        location = geolocator.geocode(location_string)
        if location:
            return location.latitude, location.longitude, location.address
        else:
            raise ValueError(f"Could not geocode location: {location_string}")
    except GeopyError as e:
        raise RuntimeError(f"Geocoding error: {e}")


def get_timezone_for_coords(lat, lng):
    """Get timezone name for coordinates"""
    if not TZ_AVAILABLE or TZ_FINDER is None:
        return None
    try:
        tz_name = TZ_FINDER.timezone_at(lat=lat, lng=lng)
        return tz_name
    except Exception:
        return None


def format_time(iso_string, timezone_name=None):
    """Format ISO time string for display in local timezone"""
    if not iso_string:
        return "—"
    
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        if timezone_name:
            try:
                local_tz = ZoneInfo(timezone_name)
                dt_local = dt.astimezone(local_tz)
                # Show time with timezone abbreviation
                return dt_local.strftime("%H:%M:%S %Z")
            except Exception:
                # Fall back to UTC if timezone conversion fails
                pass
        return dt.strftime("%H:%M:%S UTC")
    except (ValueError, TypeError):
        return iso_string


def call_suncalc_bridge(lat, lng, date_str=None):
    """Call the Node.js suncalc bridge and return results"""
    bridge_path = Path(__file__).parent / "suncalc_bridge.js"
    
    if not bridge_path.exists():
        raise FileNotFoundError(f"Bridge script not found: {bridge_path}")
    
    # Prepare input
    input_data = {
        "lat": lat,
        "lng": lng
    }
    if date_str:
        input_data["date"] = date_str
    
    # Call Node.js bridge
    try:
        result = subprocess.run(
            ["node", str(bridge_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        try:
            error_data = json.loads(error_msg)
            raise RuntimeError(f"suncalc error: {error_data.get('error', error_msg)}")
        except json.JSONDecodeError:
            raise RuntimeError(f"suncalc bridge failed: {error_msg}")
    except subprocess.TimeoutExpired:
        raise RuntimeError("suncalc bridge timed out")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse suncalc output: {e}")


def get_moon_phase_name(phase):
    """Convert moon phase value to name"""
    names = [
        'New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous',
        'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent'
    ]
    idx = round(phase * 8) % 8
    return names[idx]


def main():
    parser = argparse.ArgumentParser(
        description="Calculate sun and moon times using suncalc.js",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --lat 51.5 --lng -0.1 --date 2026-08-24
  %(prog)s --city "London, UK"
  %(prog)s --city "New York" --date "2026-06-21T12:00:00Z"
  %(prog)s --lat 40.7128 --lng -74.0060 --json
        """
    )
    
    # Location group (mutually exclusive)
    location_group = parser.add_mutually_exclusive_group(required=True)
    location_group.add_argument(
        "--lat", type=float,
        help="Latitude in decimal degrees"
    )
    location_group.add_argument(
        "--city", type=str,
        help="City name (e.g., 'London' or 'London, UK') - requires geopy"
    )
    
    parser.add_argument(
        "--lng", type=float,
        help="Longitude in decimal degrees (required with --lat)"
    )
    parser.add_argument(
        "--date", type=str,
        help="Date/time in ISO format (default: now). Examples: 2026-08-24, 2026-08-24T12:00:00Z"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Output raw JSON instead of formatted text"
    )
    parser.add_argument(
        "--no-moon", action="store_true",
        help="Skip moon calculations"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.lat is not None and args.lng is None:
        parser.error("--lng is required when using --lat")
    if args.lng is not None and args.lat is None:
        parser.error("--lat is required when using --lng")
    
    # Get coordinates
    try:
        if args.city:
            print(f"Geocoding '{args.city}'...", file=sys.stderr)
            lat, lng, address = geocode_location(args.city)
            print(f"Found: {address}", file=sys.stderr)
            print(f"Coordinates: {lat:.4f}, {lng:.4f}\n", file=sys.stderr)
        else:
            lat, lng = args.lat, args.lng
            address = None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Call suncalc
    try:
        result = call_suncalc_bridge(lat, lng, args.date)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Output JSON if requested
    if args.json:
        print(json.dumps(result, indent=2))
        return
    
    # Get timezone for coordinates
    timezone_name = get_timezone_for_coords(lat, lng)
    
    # Format human-readable output
    date_obj = datetime.fromisoformat(result["date"].replace('Z', '+00:00'))
    
    print("=" * 70)
    print(f"SunCalc Results")
    print("=" * 70)
    if address:
        print(f"Location: {address}")
    print(f"Coordinates: {lat:.6f}°N, {lng:.6f}°E")
    if timezone_name:
        print(f"Timezone: {timezone_name}")
        # Convert date to local time for display
        try:
            local_tz = ZoneInfo(timezone_name)
            date_local = date_obj.astimezone(local_tz)
            print(f"Date: {date_local.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        except Exception:
            print(f"Date: {date_obj.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    else:
        print(f"Date: {date_obj.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print()
    
    # Sun times
    print("SUN TIMES")
    print("-" * 70)
    sun = result["sun"]
    times = sun["times"]
    
    if sun["alwaysUp"]:
        print("☀️  Polar Day - Sun never sets")
    elif sun["alwaysDown"]:
        print("🌑 Polar Night - Sun never rises")
    else:
        time_labels = [
            ("Night end", "nightEnd"),
            ("Nautical dawn", "nauticalDawn"),
            ("Dawn", "dawn"),
            ("Sunrise", "sunrise"),
            ("Sunrise end", "sunriseEnd"),
            ("Golden hour end", "goldenHourEnd"),
            ("Solar noon", "solarNoon"),
            ("Golden hour", "goldenHour"),
            ("Sunset start", "sunsetStart"),
            ("Sunset", "sunset"),
            ("Dusk", "dusk"),
            ("Nautical dusk", "nauticalDusk"),
            ("Night", "night"),
        ]
        
        for label, key in time_labels:
            time_str = format_time(times.get(key), timezone_name)
            print(f"  {label:20s} {time_str}")
    
    print()
    print(f"Sun position: altitude {sun['position']['altitude']:.2f}°, "
          f"azimuth {sun['position']['azimuth']:.2f}°")
    print()
    
    # Moon times (unless disabled)
    if not args.no_moon:
        print("MOON TIMES")
        print("-" * 70)
        moon = result["moon"]
        moon_times = moon["times"]
        
        if moon["alwaysUp"]:
            print("🌕 Moon is always up")
        elif moon["alwaysDown"]:
            print("🌑 Moon is always down")
        else:
            rise = format_time(moon_times.get("rise"), timezone_name)
            set_time = format_time(moon_times.get("set"), timezone_name)
            print(f"  Moonrise: {rise}")
            print(f"  Moonset:  {set_time}")
        
        print()
        illum = moon["illumination"]
        phase_name = get_moon_phase_name(illum["phase"])
        print(f"Moon phase: {phase_name}")
        print(f"  Illumination: {illum['fraction']:.1%}")
        print(f"  Phase value: {illum['phase']:.3f}")
        print(f"  Waxing: {illum['waxing']}")
        print()
        print(f"Moon position: altitude {moon['position']['altitude']:.2f}°, "
              f"azimuth {moon['position']['azimuth']:.2f}°")
        print(f"Distance: {moon['position']['distance']:.0f} km")
    
    print("=" * 70)


if __name__ == "__main__":
    main()
