# Cricket Streamer

This project is a standalone IPTV player for macOS developed for high-stability cricket streaming. It utilizes the VLC media engine and PyQt6 for a modern, responsive user interface.

## Description

The application provides an immersive viewing experience with features such as glassmorphism-based UI controls, motion-activated control visibility, and automated stream health monitoring. It is designed to handle common IPTV stability issues through configurable network caching and automated reconnection logic.

## Key Features

- **Automated Stream Recovery**: Background monitoring to detect and resolve stream drops.
- **Dynamic UI**: Motion-sensitive control bar that hides during active playback.
- **VLC Engine Integration**: High-performance decoding for HLS/M3U8 protocols.
- **macOS Bundle**: Packaged as a native `.app` with custom icon assets.

## Implementation Details

The implementation leverages `python-vlc` for low-level media handling and `PyQt6` for the window management and event loops. The build process uses `PyInstaller` to create a self-contained application bundle.

## Installation and Build

### Prerequisites
- macOS
- [VLC Media Player](https://www.videolan.org/vlc/)
- [uv](https://github.com/astral-sh/uv) (recommended) or `pip`

### Build Process
To set up the environment and compile the application:

```bash
chmod +x setup_and_build.sh
./setup_and_build.sh
```

The resulting executable will be located in the `dist/` directory.

## Dependencies

Refer to `requirements.txt` for the full list of Python dependencies. Core libraries include:
- `PyQt6`
- `python-vlc`
- `pyinstaller`
