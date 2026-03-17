#!/bin/bash
# ---------------------------------------------------------
# Build Script for Cricket Streamer (macOS)
# ---------------------------------------------------------

# Exit on error
set -e

echo "Setting up environment..."

# 1. Setup Environment using uv if available, otherwise fallback to venv/pip
if command -v uv &> /dev/null
then
    echo "Using uv for dependency management..."
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
else
    echo "uv not found, falling back to standard venv and pip..."
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 2. Generate macOS Icon from PNG
echo "Generating macOS icon assets..."
mkdir -p icon.iconset
sips -z 16 16     app_icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     app_icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     app_icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     app_icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   app_icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   app_icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   app_icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   app_icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   app_icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 app_icon.png --out icon.iconset/icon_512x512@2x.png

iconutil -c icns icon.iconset
rm -rf icon.iconset

# 3. Build Standalone App Bundle
echo "Building standalone application..."
rm -rf build dist
pyinstaller --noconfirm --windowed --onefile \
    --name "Match Watcher" \
    --icon "icon.icns" \
    --add-data "app_icon.png:." \
    --add-data ".env:." \
    app.py

echo "---------------------------------------------------------"
echo "Build project successfully completed."
echo "Application bundle available in: dist/Match Watcher.app"
echo "---------------------------------------------------------"
