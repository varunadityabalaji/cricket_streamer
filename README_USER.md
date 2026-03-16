# Match Watcher Pro

A standalone IPTV player for macOS built with Python and PyQt6.

## Features
- **Premium UI**: Dark mode interface with a modern aesthetic.
- **Auto-Restart**: Automatically attempts to reconnect if the stream drops or encounters an error.
- **Pre-filled URL**: Starts with your provided IPTV link.
- **Standalone**: Packaged as a standard macOS `.app`.

## How to use
- Open `dist/Match Watcher.app` to run the application.
- Use the **PLAY/STOP** buttons to control the stream.
- Click **RESTART** if you want to manually refresh the connection.
- Paste any new `.m3u8` link into the input box to change channels.

## Technical Details
- **GUI Engine**: PyQt6
- **Media Engine**: QtMultimedia (uses native macOS AVFoundation)
- **Restart Logic**: Monitors playback state and reconnects on errors or unexpected stops.
- **Build Tool**: PyInstaller

## For Developers
If you want to modify the code:
1. Edit `app.py`.
2. Run `bash build_app.sh` to update the `.app` bundle.
