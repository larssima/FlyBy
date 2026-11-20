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

## Screensaver / auto power-off

The app tries two things to keep the TV awake while the radar is shown:

1. A hidden, muted, looping video — TVs normally hold off the screensaver
   during media playback.
2. It answers webOS's "may I start the screensaver?" request with *no*
   (`com.webos.service.tvpower`). Not every model/firmware allows this for
   side-loaded apps.

Neither can fake a remote button press, so the TV's legally required
**inactivity power-off** (EU: *Settings → General → Eco/Energy Saving →
Auto Power Off*) may still apply; switch it off there if it does.

## Install

The ready-built package is `dist/com.larssima.flyby_1.0.1_all.ipk`.

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
   ares-install --device tv webOS/dist/com.larssima.flyby_1.0.1_all.ipk
   ares-launch  --device tv com.larssima.flyby
   ```

Prefer a GUI? *webOS Dev Manager* (github.com/webosbrew/dev-manager-desktop)
does steps 4–5 with a few clicks.

**Dev Mode expires** after ~50 hours unless you press *Extend* in the
Developer Mode app; when it lapses, side-loaded apps stop launching.

## Rebuild after changing the app

The app's files are in `app/`. Rebuilding is only needed when something in
there changes — not for changes to the radar itself. Bump `version` in
`app/appinfo.json` first so the TV accepts the update, then from the repo root:

```
ares-package webOS/app -o webOS/dist
```

To pin the radar to a fixed spot, change `RADAR_URL` in `app/index.html` to
`https://flyby-radar.netlify.app/?lat=59.33&lon=18.07` (your coordinates).
