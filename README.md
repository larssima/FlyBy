# FlyBy

A single-file, browser-based ADS-B radar that shows live aircraft on a green sweeping radar display — no build tools, no dependencies to install.

![FlyBy radar screenshot](https://github.com/larssima/FlyBy/raw/master/Screenshot.png)

---

## What it does

- Plots real aircraft around your current location on a circular radar sweep — auto-detected via the browser's GPS, falling back to your network's approximate location
- Aircraft blips appear as the sweep passes over them and fade as they age
- Short trail dots show recent movement; a heading vector points in the direction of travel
- Clicking a blip opens a detail panel with callsign, aircraft type, manufacturer, registration, operator, and the full origin → destination route
- Live telemetry (altitude, speed, vertical rate, distance, bearing) updates every second while a flight is selected

---

## Features

| Feature | Details |
|---|---|
| **Live radar** | Sweeps every 8 seconds; aircraft data refreshed from ADS-B APIs every 10 s |
| **Range selector** | 10 km / 50 km / 100 km — switches range and re-fetches immediately |
| **MAP mode** | Toggle an OpenStreetMap background behind the radar (via Leaflet) |
| **Auto mode** | Automatically cycles through visible flights on screen — great for a wall-mounted display |
| **Auto interval** | Configurable: click the interval button to cycle through 10 s / 15 s / 30 s / 60 s / 2 m / 5 m |
| **Flight details** | Route (origin/destination airports with IATA + ICAO codes), airline, aircraft DB lookup |
| **Google Maps link** | Click the center coordinates to open your radar center in Google Maps |
| **Countdown display** | AUTO button shows remaining seconds before next aircraft is selected |

---

## Running it

Because the ADS-B APIs reject requests from `file://` origins (CORS), you must serve the file over HTTP — even locally.

```bash
# Node.js
npx serve .

# Python 3
python -m http.server 3000

# Python 2
python -m SimpleHTTPServer 3000
```

Then open [http://localhost:3000](http://localhost:3000) in your browser.

> **Raspberry Pi / kiosk:** Run `npx serve .` on boot and open Chromium in kiosk mode pointing at `http://localhost:3000`. Enable AUTO mode and it will cycle through flights hands-free.

---

## Data sources

Aircraft position data is fetched from these ADS-B aggregators (tried in order, first to respond wins):

1. [airplanes.live](https://airplanes.live)
2. [adsb.lol](https://adsb.lol)
3. [adsb.fi](https://adsb.fi)

Flight details (aircraft database + route) come from [adsbdb.com](https://adsbdb.com).

All sources are free and open — no API keys required.

---

## Setting the radar location

By default, FlyBy centers on your current location:

1. **Browser GPS** — prompts for location permission on first load
2. **IP geolocation** ([ipapi.co](https://ipapi.co)) — used if GPS is denied or unavailable
3. **London** — final fallback if both fail

To pin a specific location (e.g. for a wall-mounted display):

- Click the **SET** button next to the coordinates, then paste a Google Maps link (`.../@59.33,18.07,12z` or `?q=59.33,18.07`) or plain `lat,lon` coordinates. This is saved in the browser (`localStorage`) and used on every future load. Leave the prompt empty to clear it and go back to auto-detection.
- Or append `?lat=59.33&lon=18.07` to the URL — useful for bookmarking a fixed kiosk location. This takes priority over the saved location.

---

## Configuration

Open `index.html` and adjust these constants near the top of the script:

| Constant | Default | Description |
|---|---|---|
| `RADIUS_KM` | `100` | Initial radar range in km |
| `SWEEP_SPEED` | `2π / 8` | One full rotation every 8 seconds |
| `FETCH_EVERY` | `10000` | API poll interval in milliseconds |
| `STALE_HIDE` | `20` | Hide aircraft not heard for this many seconds |
| `AUTO_INTERVALS` | `[10,15,30,60,120,300]` | Available auto-cycle intervals (seconds) |

---

## Project structure

```
FlyBy/
└── index.html   # Entire application — HTML, CSS, and JavaScript in one file
```

No framework, no bundler, no package.json. Drop it on any static file server and it works.
