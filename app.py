import sys
import os
import platform
import ctypes
import vlc
import logging
from dotenv import load_dotenv

# Load environment variables
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

load_dotenv(resource_path(".env"))
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QPushButton, QLabel, 
                             QSlider, QFrame, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, QTimer, QPoint, QEvent
from PyQt6.QtGui import QColor, QPalette, QFont, QIcon

# Logging Setup
log_file = "/tmp/match_watcher.log"
logging.basicConfig(filename=log_file, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def setup_vlc_path():
    if platform.system() == "Darwin":
        vlc_paths = [
            "/Applications/VLC.app/Contents/MacOS/lib/libvlc.dylib",
            "/opt/homebrew/lib/libvlc.dylib",
            "/usr/local/lib/libvlc.dylib",
        ]
        for path in vlc_paths:
            if os.path.exists(path):
                os.environ['PYTHON_VLC_LIB_PATH'] = path
                return True
    return False

setup_vlc_path()

class GlassButton(QPushButton):
    def __init__(self, text, color="#007AFF"):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(45) # Enforce a solid height
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color}dd;
                color: white;
                border-radius: 12px;
                padding: 5px 20px;
                font-weight: 800;
                font-size: 14px;
                border: 1px solid rgba(255,255,255,0.2);
            }}
            QPushButton:hover {{
                background-color: {color};
                border: 1px solid white;
            }}
        """)

class IPTVPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Match Watcher Pro")
        self.setWindowIcon(QIcon(resource_path("app_icon.png")))
        self.resize(1100, 750)
        self.setMinimumSize(850, 600)
        
        # Channel Config
        self.channels = {
            "TAMIL": os.getenv("TAMIL_STREAM_URL", ""),
            "ENGLISH": os.getenv("ENGLISH_STREAM_URL", "")
        }
        self.current_channel = "TAMIL"
        
        # Link state - Use the first available or default to empty
        self.default_url = self.channels.get("TAMIL") or ""
        
        # VLC Setup - Optimized for faster start
        args = [
            '--no-video-title-show',
            '--network-caching=2000',
            '--quiet'
        ]
        try:
            self.instance = vlc.Instance(args)
            self.vlc_player = self.instance.media_player_new()
        except Exception as e:
            logging.error(f"VLC Init Error: {e}")
            sys.exit(1)
            
        # UI State
        self.is_playing_requested = False
        self.controls_visible = True
        
        # UI Setup
        self.init_ui()
        
        # Timers
        self.hide_timer = QTimer()
        self.hide_timer.setInterval(4000) # Slightly longer hide time
        self.hide_timer.timeout.connect(self.hide_controls)
        
        self.health_timer = QTimer()
        self.health_timer.timeout.connect(self.check_stream)
        self.health_timer.start(5000)
        
        # Mouse Tracking
        self.setMouseTracking(True)
        self.centralWidget().setMouseTracking(True)
        self.video_container.setMouseTracking(True)
        
        # Mac embedding
        QTimer.singleShot(500, self.embed_vlc)

    def init_ui(self):
        self.container = QWidget()
        self.setCentralWidget(self.container)
        self.setStyleSheet("background-color: #000;")
        
        # Video Frame (Full Size)
        self.video_container = QFrame(self.container)
        self.video_container.setStyleSheet("background-color: #000;")
        self.video_container.setGeometry(self.rect())
        
        # Overlay Control Bar
        self.overlay = QFrame(self.container)
        self.overlay.setObjectName("ControlPanel")
        self.overlay.setStyleSheet("""
            QFrame#ControlPanel {
                background-color: rgba(15, 15, 15, 230);
                border-radius: 24px;
                border: 1px solid rgba(255,255,255,0.15);
            }
            QLineEdit {
                background-color: rgba(30, 30, 30, 255);
                color: #fff;
                border-radius: 10px;
                padding: 10px;
                border: 1px solid #444;
                font-size: 13px;
            }
            QLabel { color: #eee; font-size: 12px; font-weight: 700; }
        """)
        
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setContentsMargins(25, 20, 25, 20)
        overlay_layout.setSpacing(15)
        
        # Row 1: URL
        top_row = QHBoxLayout()
        self.url_input = QLineEdit(self.default_url)
        top_row.addWidget(QLabel("STREAM SOURCE:"))
        top_row.addWidget(self.url_input, 1)
        
        # Row 1.5: Channel Selection
        chan_row = QHBoxLayout()
        chan_row.setSpacing(10)
        chan_row.addWidget(QLabel("CHANNEL:"))
        
        self.tamil_btn = QPushButton("TAMIL")
        self.english_btn = QPushButton("ENGLISH")
        
        for btn in [self.tamil_btn, self.english_btn]:
            btn.setCheckable(True)
            btn.setFixedHeight(30)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.1);
                    color: #fff;
                    border-radius: 6px;
                    padding: 0 15px;
                    font-size: 11px;
                    font-weight: bold;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                QPushButton:checked {
                    background-color: #007AFF;
                    border: 1px solid #007AFF;
                }
                QPushButton:hover:not(:checked) {
                    background-color: rgba(255,255,255,0.2);
                }
            """)
        
        self.tamil_btn.setChecked(True)
        self.tamil_btn.clicked.connect(lambda: self.switch_channel("TAMIL"))
        self.english_btn.clicked.connect(lambda: self.switch_channel("ENGLISH"))
        
        chan_row.addWidget(self.tamil_btn)
        chan_row.addWidget(self.english_btn)
        chan_row.addStretch()
        
        # Row 2: Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(15)
        self.play_btn = GlassButton("▶  PLAY", "#22C55E")
        self.stop_btn = GlassButton("⏹  STOP", "#EF4444")
        self.restart_btn = GlassButton("↺  RELOAD", "#F59E0B")
        
        self.play_btn.clicked.connect(self.play_stream)
        self.stop_btn.clicked.connect(self.stop_stream)
        self.restart_btn.clicked.connect(self.reload_stream)
        
        btn_row.addWidget(self.play_btn)
        btn_row.addWidget(self.stop_btn)
        btn_row.addWidget(self.restart_btn)
        
        # Row 3: Vol & Status
        bottom_row = QHBoxLayout()
        self.status_label = QLabel("SYSTEM IDLE")
        self.status_label.setStyleSheet("color: #777; font-family: 'Menlo';")
        
        self.vol_slider = QSlider(Qt.Orientation.Horizontal)
        self.vol_slider.setRange(0, 100)
        self.vol_slider.setValue(80)
        self.vol_slider.setFixedWidth(160)
        self.vol_slider.valueChanged.connect(self.update_volume)
        
        bottom_row.addWidget(self.status_label)
        bottom_row.addStretch()
        bottom_row.addWidget(QLabel("🔊"))
        bottom_row.addWidget(self.vol_slider)
        
        overlay_layout.addLayout(top_row)
        overlay_layout.addLayout(chan_row)
        overlay_layout.addLayout(btn_row)
        overlay_layout.addLayout(bottom_row)
        
        self.update_overlay_pos()

    def resizeEvent(self, event):
        self.video_container.setGeometry(self.rect())
        self.update_overlay_pos()
        super().resizeEvent(event)

    def update_overlay_pos(self):
        w = min(900, self.width() - 80)
        h = 220 # Increased height for channel row
        x = (self.width() - w) // 2
        y = self.height() - h - 40
        self.overlay.setGeometry(x, y, w, h)

    def switch_channel(self, channel_name):
        self.current_channel = channel_name
        url = self.channels.get(channel_name, "")
        
        # Update UI buttons state
        self.tamil_btn.setChecked(channel_name == "TAMIL")
        self.english_btn.setChecked(channel_name == "ENGLISH")
        
        if not url:
            self.status_label.setText(f"ERROR: {channel_name} LINK MISSING")
            QMessageBox.warning(self, "Link Missing", 
                              f"The {channel_name} stream link was not found in your .env file.")
            return

        self.url_input.setText(url)
        self.status_label.setText(f"SWITCHING TO {channel_name}...")
        self.play_stream()

    def embed_vlc(self):
        if platform.system() == "Darwin":
            self.vlc_player.set_nsobject(int(self.video_container.winId()))
        else:
            self.vlc_player.set_hwnd(int(self.video_container.winId()))

    def show_controls(self):
        self.overlay.show()
        self.controls_visible = True
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self.hide_timer.start()

    def hide_controls(self):
        if self.is_playing_requested and not self.overlay.underMouse():
            self.overlay.hide()
            self.controls_visible = False
            self.setCursor(Qt.CursorShape.BlankCursor)
            self.hide_timer.stop()

    def mouseMoveEvent(self, event):
        self.show_controls()
        super().mouseMoveEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
        super().mouseDoubleClickEvent(event)

    def play_stream(self):
        url = self.url_input.text().strip()
        if url:
            media = self.instance.media_new(url)
            self.vlc_player.set_media(media)
            self.vlc_player.play()
            self.is_playing_requested = True
            self.status_label.setText("CONNECTING...")
            self.hide_timer.start()

    def stop_stream(self):
        # Fix: Stop in a way that doesn't hang the UI
        self.is_playing_requested = False
        self.status_label.setText("STOPPING...")
        # VLC stop can block, we can just pause and release if needed, 
        # or call stop. Let's try to ensure it doesn't hang.
        QTimer.singleShot(10, self.vlc_player.stop)
        self.status_label.setText("STOPPED")
        self.show_controls()

    def reload_stream(self):
        self.vlc_player.stop()
        QTimer.singleShot(800, self.play_stream)

    def update_volume(self, val):
        self.vlc_player.audio_set_volume(val)

    def check_stream(self):
        if not self.is_playing_requested:
            return
        state = self.vlc_player.get_state()
        if state == vlc.State.Playing:
            self.status_label.setText("LIVE")
            self.status_label.setStyleSheet("color: #28a745;")
        elif state == vlc.State.Buffering:
            self.status_label.setText("BUFFERING...")
        elif state in [vlc.State.Error, vlc.State.Ended]:
            self.play_stream()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = IPTVPlayer()
    player.show()
    sys.exit(app.exec())
