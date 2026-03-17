# Match Watcher Pro 🏏

A simple and stable IPTV player for macOS, specially designed for watching cricket streams without interruptions.

![App Icon](app_icon.png)

## What is this?
This is a standalone macOS app that lets you stream IPTV links (like `.m3u8`). It uses the powerful VLC engine behind the scenes to make sure the stream stays smooth and automatically reconnects if the connection drops.

## Features
- **Modern Design**: A clean, dark-mode interface that stays out of your way.
- **Auto-Fix**: If the stream stops or lags, the app automatically tries to reload it for you.
- **Easy Controls**: Play, Stop, and Reload buttons with a simple volume slider.
- **Full Screen**: Double-click the video to go full screen.

## How to Install and Run

### 1. Prerequisites
Before you start, make sure you have these two things installed on your Mac:
1. **VLC Media Player**: The app needs VLC's engine to work.
   ```bash
   brew install --cask vlc
   ```
2. **Python**: Make sure you have Python 3 installed.

### 2. Quick Start (Running Locally)
If you just want to run the app right now:
```bash
# Install the required libraries
pip install -r requirements.txt

# Start the app
python3 app.py
```

### 3. Build the Standalone App
If you want to create a real `.app` file that you can keep in your Applications folder:
```bash
# This script sets everything up and builds the app for you
chmod +x setup_and_build.sh
./setup_and_build.sh
```
Once it's done, you'll find **Match Watcher.app** inside the `dist` folder.

## How to Use
1. Paste your IPTV or `.m3u8` link into the **STREAM SOURCE** box.
2. Click **PLAY**.
3. If the stream ever gets stuck, click **RELOAD** to refresh it manually.
4. Move your mouse to see the controls; they will hide automatically while you're watching.
