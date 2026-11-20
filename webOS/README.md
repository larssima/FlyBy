# FlyBy for LG webOS TV

A small "hosted" webOS app: the TV opens https://flyby-radar.netlify.app/
full screen. The radar runs natively on the TV (no streaming blur), and every
push to `master` reaches the TV without reinstalling.

## Remote control

| Button      | Action                              |
|-------------|-------------------------------------|
| Red         | Cycle range (10 / 50 / 100 km)      |
| Green       | AUTO on/off                         |
| Yellow      | Airports (APT) on/off               |
| Blue        | Labels (LBL) on/off                 |
| ◀ / ▶       | Previous / next aircraft (nearest first) |
| Pointer     | Click blips and buttons as usual    |

## Install

The ready-built package is `dist/com.larssima.flyby_1.0.0_all.ipk`.

1. Create a free account at https://webostv.developer.lge.com.
2. On the TV, install **Developer Mode** from the LG Content Store, log in,
   turn on *Dev Mode Status* and restart the TV. Turn on *Key Server*.
3. On your computer install the CLI: `npm install -g @webos-tools/cli`
4. Register the TV (it must be on the same network):
   ```
   ares-setup-device            # add device: name "tv", the TV's IP, port 9922, user prisoner
   ares-novacom --device tv --getkey   # enter the passphrase shown in Developer Mode
   ```
5. Install and launch:
   ```
   ares-install --device tv webOS/dist/com.larssima.flyby_1.0.0_all.ipk
   ares-launch  --device tv com.larssima.flyby
   ```

Prefer a GUI? *webOS Dev Manager* (github.com/webosbrew/dev-manager-desktop)
does steps 4–5 with a few clicks.

**Dev Mode expires** after ~50 hours unless you press *Extend* in the
Developer Mode app; when it lapses, side-loaded apps stop launching.

## Rebuild after changing this folder

Only needed when `appinfo.json`, `index.html` or the icons here change — not
for changes to the radar itself.

```
ares-package webOS -o webOS/dist -e dist -e README.md
```

Bump `version` in `appinfo.json` first so the TV accepts the update.

To pin the radar to a fixed spot, change `RADAR_URL` in `index.html` to
`https://flyby-radar.netlify.app/?lat=59.33&lon=18.07` (your coordinates).
