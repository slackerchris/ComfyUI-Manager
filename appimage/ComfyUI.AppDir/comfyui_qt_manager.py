#!/usr/bin/env python3
"""
ComfyUI Qt Manager - Professional Native Desktop Interface
A proper, native desktop application for managing ComfyUI with Qt/PySide6
"""

import sys
import os
import json
import subprocess
import psutil
import threading
import time
from pathlib import Path
from typing import Optional, Dict, List

# Configure Qt platform for AppImage compatibility BEFORE importing Qt
def setup_qt_platform():
    """Configure Qt platform for optimal AppImage compatibility"""
    print(f"🔧 Configuring Qt platform...")
    print(f"   XDG_SESSION_TYPE: {os.environ.get('XDG_SESSION_TYPE', 'Not set')}")
    print(f"   WAYLAND_DISPLAY: {os.environ.get('WAYLAND_DISPLAY', 'Not set')}")
    
    # Check if we're in Wayland environment
    if os.environ.get('XDG_SESSION_TYPE') == 'wayland' or os.environ.get('WAYLAND_DISPLAY'):
        os.environ['QT_QPA_PLATFORM'] = 'wayland'
        print("   ✅ Configured Qt for Wayland platform")
    else:
        # For X11, set compatibility options to prevent crashes
        os.environ['QT_X11_NO_MITSHM'] = '1'
        print("   ✅ Configured Qt for X11 platform with compatibility options")

# Set up Qt platform before any Qt imports
setup_qt_platform()

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QPushButton, QTextEdit, QProgressBar,
        QSystemTrayIcon, QMenu, QFileDialog, QMessageBox, QGroupBox,
        QStatusBar, QTabWidget, QListWidget, QListWidgetItem, QSplitter,
        QFrame, QScrollArea, QCheckBox, QSpinBox, QLineEdit, QComboBox
    )
    from PySide6.QtCore import Qt, QTimer, QThread, Signal, QSize, QSettings
    from PySide6.QtGui import QIcon, QFont, QPixmap, QAction, QPalette
except ImportError:
    print("Error: PySide6 not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QLabel, QPushButton, QTextEdit, QProgressBar,
        QSystemTrayIcon, QMenu, QFileDialog, QMessageBox, QGroupBox,
        QStatusBar, QTabWidget, QListWidget, QListWidgetItem, QSplitter,
        QFrame, QScrollArea, QCheckBox, QSpinBox, QLineEdit, QComboBox
    )
    from PySide6.QtCore import Qt, QTimer, QThread, Signal, QSize, QSettings
    from PySide6.QtGui import QIcon, QFont, QPixmap, QAction, QPalette


class ProcessMonitor(QThread):
    """Background thread for monitoring ComfyUI processes"""
    process_updated = Signal(dict)
    
    def __init__(self):
        super().__init__()
        self.running = True
        
    def run(self):
        while self.running:
            try:
                processes = self.get_comfyui_status()
                self.process_updated.emit(processes)
                self.msleep(1000)  # Update every second
            except Exception as e:
                print(f"Process monitor error: {e}")
                
    def stop(self):
        self.running = False
        
    def get_comfyui_status(self) -> Dict:
        """Get detailed ComfyUI process status with statistics"""
        processes = []
        total_memory = 0
        total_cpu = 0
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(keyword in cmdline.lower() for keyword in ['comfyui', 'main.py']):
                        if 'ComfyUI' in cmdline or 'main.py' in cmdline:
                            cpu_percent = proc.cpu_percent()
                            memory_mb = proc.info['memory_info'].rss / 1024 / 1024
                            
                            processes.append({
                                'pid': proc.info['pid'],
                                'name': proc.info['name'],
                                'cmdline': cmdline,
                                'cpu': cpu_percent,
                                'memory': memory_mb
                            })
                            
                            total_memory += memory_mb
                            total_cpu += cpu_percent
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"Error finding processes: {e}")
            
        return {
            'processes': processes,
            'count': len(processes),
            'total_memory': total_memory,
            'total_cpu': total_cpu,
            'running': len(processes) > 0
        }


class ModelManager(QWidget):
    """Professional model management interface"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.models_dir = Path.home() / ".local" / "share" / "ComfyUI"
        self.setup_ui()
        self.refresh_models()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Models directory section
        dir_group = QGroupBox("Models Directory")
        dir_layout = QHBoxLayout(dir_group)
        
        self.dir_label = QLabel(str(self.models_dir))
        self.dir_label.setStyleSheet("padding: 5px; border: 1px solid gray;")
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_models_dir)
        
        open_btn = QPushButton("Open in File Manager")
        open_btn.clicked.connect(self.open_models_dir)
        
        dir_layout.addWidget(self.dir_label, 1)
        dir_layout.addWidget(browse_btn)
        dir_layout.addWidget(open_btn)
        
        layout.addWidget(dir_group)
        
        # Models list
        models_group = QGroupBox("Available Models")
        models_layout = QVBoxLayout(models_group)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Models List")
        refresh_btn.clicked.connect(self.refresh_models)
        models_layout.addWidget(refresh_btn)
        
        # Models list widget
        self.models_list = QListWidget()
        self.models_list.setAlternatingRowColors(True)
        models_layout.addWidget(self.models_list)
        
        layout.addWidget(models_group)
        
    def browse_models_dir(self):
        """Browse for models directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Models Directory", str(self.models_dir)
        )
        if dir_path:
            self.models_dir = Path(dir_path)
            self.dir_label.setText(str(self.models_dir))
            self.refresh_models()
            
    def open_models_dir(self):
        """Open models directory in file manager"""
        if not self.models_dir.exists():
            self.models_dir.mkdir(parents=True, exist_ok=True)
        subprocess.Popen(['xdg-open', str(self.models_dir)])
        
    def refresh_models(self):
        """Refresh the models list"""
        self.models_list.clear()
        
        if not self.models_dir.exists():
            self.models_dir.mkdir(parents=True, exist_ok=True)
            
        # Create model subdirectories
        model_dirs = ['checkpoints', 'vae', 'loras', 'embeddings', 'controlnet', 'animatediff', 'video_models']
        for model_dir in model_dirs:
            dir_path = self.models_dir / model_dir
            dir_path.mkdir(exist_ok=True)
            
            # Add directory header
            header_item = QListWidgetItem(f"📁 {model_dir.upper()}")
            header_item.setFont(QFont("", -1, QFont.Bold))
            header_item.setBackground(QPalette().alternateBase())
            self.models_list.addItem(header_item)
            
            # Add models in directory
            try:
                model_files = list(dir_path.glob("*"))
                if model_files:
                    for model_file in sorted(model_files):
                        if model_file.is_file():
                            size_mb = model_file.stat().st_size / 1024 / 1024
                            item_text = f"  🔧 {model_file.name} ({size_mb:.1f} MB)"
                            self.models_list.addItem(QListWidgetItem(item_text))
                else:
                    self.models_list.addItem(QListWidgetItem("  (no models found)"))
            except Exception as e:
                self.models_list.addItem(QListWidgetItem(f"  Error: {e}"))


class ComfyUIManager(QMainWindow):
    """Professional ComfyUI Management Application"""
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings("ComfyUI", "Manager")
        self.comfyui_process = None
        self.appdir = os.environ.get('APPDIR', os.path.dirname(os.path.abspath(__file__)))
        
        self.setup_ui()
        self.setup_system_tray()
        self.setup_monitoring()
        self.load_settings()
        
    def setup_ui(self):
        """Setup the main user interface"""
        self.setWindowTitle("ComfyUI Manager")
        self.setMinimumSize(800, 600)
        
        # Apply clean, system-consistent styling
        self.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
                min-width: 100px;
                font-weight: bold;
            }
            QPushButton:disabled {
                color: #888888;
            }
        """)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Control tab
        self.setup_control_tab()
        
        # Models tab
        self.setup_models_tab()
        
        # Logs tab
        self.setup_logs_tab()
        
        # Settings tab
        self.setup_settings_tab()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def setup_control_tab(self):
        """Setup the main control interface"""
        control_widget = QWidget()
        layout = QVBoxLayout(control_widget)
        
        # Status section
        status_group = QGroupBox("ComfyUI Status")
        status_layout = QGridLayout(status_group)
        
        self.status_label = QLabel("🔴 Not Running")
        self.status_label.setFont(QFont("", 14, QFont.Bold))
        self.status_label.setAlignment(Qt.AlignCenter)
        
        self.process_info_label = QLabel("No processes found")
        self.memory_label = QLabel("Memory: 0 MB")
        self.cpu_label = QLabel("CPU: 0%")
        
        status_layout.addWidget(self.status_label, 0, 0, 1, 2)
        status_layout.addWidget(self.process_info_label, 1, 0, 1, 2)
        status_layout.addWidget(self.memory_label, 2, 0)
        status_layout.addWidget(self.cpu_label, 2, 1)
        
        layout.addWidget(status_group)
        
        # Control buttons
        controls_group = QGroupBox("Process Control")
        controls_layout = QHBoxLayout(controls_group)
        
        self.start_btn = QPushButton("▶ Start ComfyUI")
        self.start_btn.clicked.connect(self.start_comfyui)
        
        self.stop_btn = QPushButton("⏹ Stop ComfyUI")
        self.stop_btn.clicked.connect(self.stop_comfyui)
        
        self.restart_btn = QPushButton("🔄 Restart ComfyUI")
        self.restart_btn.clicked.connect(self.restart_comfyui)
        
        self.kill_btn = QPushButton("⚡ Kill All")
        self.kill_btn.clicked.connect(self.kill_all_comfyui)
        
        controls_layout.addWidget(self.start_btn)
        controls_layout.addWidget(self.stop_btn)
        controls_layout.addWidget(self.restart_btn)
        controls_layout.addWidget(self.kill_btn)
        
        layout.addWidget(controls_group)
        
        # Web interface section
        web_group = QGroupBox("Web Interface")
        web_layout = QHBoxLayout(web_group)
        
        self.web_btn = QPushButton("🌐 Open Web Interface")
        self.web_btn.clicked.connect(self.open_web_interface)
        
        self.url_label = QLabel("http://127.0.0.1:8188")
        self.url_label.setStyleSheet("padding: 5px; border: 1px solid gray; border-radius: 3px;")
        
        web_layout.addWidget(self.web_btn)
        web_layout.addWidget(self.url_label, 1)
        
        layout.addWidget(web_group)
        
        # Add stretch to push everything to top
        layout.addStretch()
        
        self.tabs.addTab(control_widget, "🎮 Control")
        
    def setup_models_tab(self):
        """Setup the models management tab"""
        self.model_manager = ModelManager(self)
        self.tabs.addTab(self.model_manager, "📁 Models")
        
    def setup_logs_tab(self):
        """Setup the logs viewing tab"""
        logs_widget = QWidget()
        layout = QVBoxLayout(logs_widget)
        
        # Log controls
        controls_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Logs")
        clear_btn.clicked.connect(self.clear_logs)
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_logs)
        
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(refresh_btn)
        controls_layout.addStretch()
        
        layout.addLayout(controls_layout)
        
        # Log display
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFont(QFont("Consolas", 10))
        layout.addWidget(self.log_display)
        
        self.tabs.addTab(logs_widget, "📋 Logs")
        
    def setup_settings_tab(self):
        """Setup the settings tab"""
        settings_widget = QWidget()
        layout = QVBoxLayout(settings_widget)
        
        # Auto-start settings
        autostart_group = QGroupBox("Auto-Start Settings")
        autostart_layout = QVBoxLayout(autostart_group)
        
        self.autostart_check = QCheckBox("Start ComfyUI when manager opens")
        self.minimize_tray_check = QCheckBox("Minimize to system tray on close")
        self.auto_open_browser_check = QCheckBox("Auto-open web interface")
        
        autostart_layout.addWidget(self.autostart_check)
        autostart_layout.addWidget(self.minimize_tray_check)
        autostart_layout.addWidget(self.auto_open_browser_check)
        
        layout.addWidget(autostart_group)
        
        # Connection settings
        connection_group = QGroupBox("Connection Settings")
        connection_layout = QGridLayout(connection_group)
        
        connection_layout.addWidget(QLabel("Host:"), 0, 0)
        self.host_input = QLineEdit("127.0.0.1")
        connection_layout.addWidget(self.host_input, 0, 1)
        
        connection_layout.addWidget(QLabel("Port:"), 1, 0)
        self.port_input = QSpinBox()
        self.port_input.setRange(1024, 65535)
        self.port_input.setValue(8188)
        connection_layout.addWidget(self.port_input, 1, 1)
        
        layout.addWidget(connection_group)
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        
        self.tabs.addTab(settings_widget, "⚙️ Settings")
        
    def setup_system_tray(self):
        """Setup system tray integration"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
            
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = QAction("Show Manager", self)
        show_action.triggered.connect(self.show)
        
        start_action = QAction("Start ComfyUI", self)
        start_action.triggered.connect(self.start_comfyui)
        
        stop_action = QAction("Stop ComfyUI", self)
        stop_action.triggered.connect(self.stop_comfyui)
        
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)
        
        tray_menu.addAction(show_action)
        tray_menu.addSeparator()
        tray_menu.addAction(start_action)
        tray_menu.addAction(stop_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.tray_icon_activated)
        
        # Set tray icon with proper identification
        icon = self.create_tray_icon()
        self.tray_icon.setIcon(icon)
        
        # Set detailed tooltip for system identification  
        self.tray_icon.setToolTip("ComfyUI Manager v2.0.5\nProfessional Desktop Interface for ComfyUI")
        
        # Show tray icon
        self.tray_icon.show()
        print("✅ System tray icon initialized with ComfyUI Manager branding")
        
    def create_tray_icon(self):
        """Create ComfyUI tray icon"""
        # Try to load our custom ComfyUI icon first
        app_dir = os.getenv('APPDIR', os.path.dirname(os.path.abspath(__file__)))
        icon_paths = [
            os.path.join(app_dir, 'comfyui.png'),
            os.path.join(app_dir, 'comfyui.svg'),
            os.path.join(os.path.dirname(__file__), 'comfyui.png'),
            os.path.join(os.path.dirname(__file__), 'comfyui.svg')
        ]
        
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                return QIcon(icon_path)
        
        # Fallback: Create a ComfyUI-themed icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        
        # Draw a simple ComfyUI node-like icon
        from PySide6.QtGui import QPainter, QPen, QBrush
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background circle
        painter.setBrush(QBrush(Qt.darkBlue))
        painter.setPen(QPen(Qt.blue, 2))
        painter.drawEllipse(4, 4, 24, 24)
        
        # Draw node connections
        painter.setPen(QPen(Qt.white, 2))
        painter.drawLine(8, 12, 16, 12)  # Input
        painter.drawLine(16, 20, 24, 20)  # Output
        
        # Draw central node
        painter.setBrush(QBrush(Qt.cyan))
        painter.drawEllipse(12, 8, 8, 8)
        
        painter.end()
        return QIcon(pixmap)
        
    def setup_monitoring(self):
        """Setup process monitoring"""
        self.process_monitor = ProcessMonitor()
        self.process_monitor.process_updated.connect(self.update_process_info)
        self.process_monitor.start()
        
        # Update timer for UI refresh
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_ui_state)
        self.update_timer.start(1000)
        
    def update_process_info(self, process_info: Dict):
        """Update process information display"""
        self.process_info = process_info
        
        if process_info['running']:
            self.status_label.setText("🟢 Running")
            
            count = process_info['count']
            memory = process_info['total_memory']
            cpu = process_info['total_cpu']
            
            self.process_info_label.setText(f"Processes: {count}")
            self.memory_label.setText(f"Memory: {memory:.1f} MB")
            self.cpu_label.setText(f"CPU: {cpu:.1f}%")
            
            # Update tray tooltip with running status
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.setToolTip(f"ComfyUI Manager v2.0.7 - Running ({count} processes)\nProfessional Desktop Interface for ComfyUI")
            
        else:
            self.status_label.setText("🔴 Not Running")
            self.process_info_label.setText("No processes found")
            self.memory_label.setText("Memory: 0 MB")
            self.cpu_label.setText("CPU: 0%")
            
            # Update tray tooltip with stopped status
            if hasattr(self, 'tray_icon') and self.tray_icon:
                self.tray_icon.setToolTip("ComfyUI Manager v2.0.7 - Stopped\nProfessional Desktop Interface for ComfyUI")
            
    def update_ui_state(self):
        """Update UI button states based on process status"""
        running = getattr(self, 'process_info', {}).get('running', False)
        
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)
        self.restart_btn.setEnabled(running)
        self.web_btn.setEnabled(running)
        
        # Update status bar
        if running:
            self.status_bar.showMessage("ComfyUI is running")
        else:
            self.status_bar.showMessage("ComfyUI is stopped")
            
    def start_comfyui(self):
        """Start ComfyUI process"""
        try:
            if getattr(self, 'process_info', {}).get('running', False):
                QMessageBox.information(self, "Already Running", "ComfyUI is already running!")
                return
                
            # Prevent multiple simultaneous start attempts
            if hasattr(self, 'comfyui_process') and self.comfyui_process is not None:
                if self.comfyui_process.poll() is None:  # Still running
                    self.log_display.append("⚠️ ComfyUI is already starting/running")
                    return
                
            self.log_display.append("🚀 Preparing to start ComfyUI...")
            
            # Build command - use AppImage Python with real ComfyUI
            # Try to find the extracted AppImage Python first
            extracted_python_locations = [
                "/home/chris/Documents/Git/Projects/ComfyUI/appimage/squashfs-root/usr/bin/python3",
                os.path.join(self.appdir, "usr", "bin", "python3")
            ]
            
            appimage_python = None
            for py_location in extracted_python_locations:
                if os.path.exists(py_location):
                    appimage_python = py_location
                    break
            
            if appimage_python:
                # Use AppImage Python (embedded or extracted)
                python_exe = appimage_python
                self.log_display.append(f"🔧 Using AppImage Python: {python_exe}")
                
                # Use real ComfyUI installation, not AppImage's copy
                main_py = "/home/chris/Documents/Git/Projects/ComfyUI/main.py"
                if os.path.exists(main_py):
                    self.log_display.append(f"🔧 Using real ComfyUI at: {main_py}")
                else:
                    # Fallback to AppImage's ComfyUI
                    main_py = os.path.join(self.appdir, "app", "main.py")
                    self.log_display.append(f"🔧 Using AppImage ComfyUI at: {main_py}")
            else:
                # Ultimate fallback - system Python
                python_exe = sys.executable
                main_py = "/home/chris/Documents/Git/Projects/ComfyUI/main.py"
                self.log_display.append(f"⚠️ Fallback to system Python: {python_exe}")
            
            # Validate paths exist
            if not os.path.exists(python_exe):
                raise FileNotFoundError(f"Python executable not found: {python_exe}")
            if not os.path.exists(main_py):
                raise FileNotFoundError(f"ComfyUI main.py not found: {main_py}")
            
            host = self.host_input.text()
            port = self.port_input.value()
            
            cmd = [
                python_exe, main_py,
                "--listen", host,
                "--port", str(port),
                "--user-directory", str(Path.home() / ".config" / "ComfyUI")
            ]
            
            if self.auto_open_browser_check.isChecked():
                cmd.append("--auto-launch")
                
            self.log_display.append(f"📋 Command: {' '.join(cmd[:3])} [args...]")
                
            # Set environment carefully - different for AppImage vs development
            env = os.environ.copy()
            
            if appimage_python and python_exe == appimage_python:
                # Using AppImage Python - set up AppImage environment
                if "/squashfs-root/" in python_exe:
                    # Using extracted AppImage
                    appimage_root = "/home/chris/Documents/Git/Projects/ComfyUI/appimage/squashfs-root"
                    env.update({
                        'PYTHONHOME': os.path.join(appimage_root, "usr"),
                        'PYTHONPATH': os.path.join(appimage_root, "usr", "lib", "python3.12", "site-packages"),
                        'LD_LIBRARY_PATH': os.path.join(appimage_root, "usr", "lib"),
                    })
                    self.log_display.append("🔧 Using extracted AppImage Python environment")
                else:
                    # Using AppImage from AppDir
                    env.update({
                        'PYTHONHOME': os.path.join(self.appdir, "usr"),
                        'PYTHONPATH': os.path.join(self.appdir, "usr", "lib", "python3.12", "site-packages"),
                        'LD_LIBRARY_PATH': os.path.join(self.appdir, "usr", "lib"),
                    })
                    self.log_display.append("🔧 Using AppImage Python environment")
            else:
                # Using system Python - clean environment
                env.pop('PYTHONHOME', None)
                env.pop('APPDIR', None)
                self.log_display.append("🔧 Using system Python environment")
            
            # Use the directory where ComfyUI main.py is located
            working_dir = os.path.dirname(main_py)
            
            # Common environment settings for both modes
            env.update({
                # Prevent Qt conflicts
                'QT_PLUGIN_PATH': '',
                'QML2_IMPORT_PATH': '',
                # Prevent process inheritance issues
                'PYTHONDONTWRITEBYTECODE': '1'
            })
            
            self.log_display.append("🔧 Environment configured, starting process...")
            
            # Start process with careful isolation
            try:
                # Try with process isolation first
                self.comfyui_process = subprocess.Popen(
                    cmd, 
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,  # Separate stderr to avoid blocking
                    text=True,
                    start_new_session=True,  # Start in new process group
                    preexec_fn=os.setsid if hasattr(os, 'setsid') else None  # Unix process isolation
                )
            except Exception as preexec_error:
                self.log_display.append(f"⚠️ Process isolation failed, trying without: {preexec_error}")
                # Fallback: start without preexec_fn
                self.comfyui_process = subprocess.Popen(
                    cmd, 
                    cwd=working_dir,
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    start_new_session=True
                )
            
            self.log_display.append(f"✅ Started ComfyUI (PID: {self.comfyui_process.pid})")
            self.status_bar.showMessage(f"ComfyUI starting (PID: {self.comfyui_process.pid})")
            
            # Monitor the process startup
            QTimer.singleShot(2000, self.check_startup_success)
            
        except Exception as e:
            error_msg = f"Failed to start ComfyUI: {str(e)}"
            self.log_display.append(f"❌ {error_msg}")
            QMessageBox.critical(self, "Start Error", error_msg)
            print(f"ComfyUI Manager - Start Error: {e}")  # Debug output
    
    def check_startup_success(self):
        """Check if ComfyUI started successfully"""
        try:
            if hasattr(self, 'comfyui_process') and self.comfyui_process:
                return_code = self.comfyui_process.poll()
                if return_code is not None:
                    # Process has already terminated - don't auto-restart to avoid loops
                    stdout, stderr = self.comfyui_process.communicate()
                    self.log_display.append(f"❌ ComfyUI failed to start (exit code: {return_code})")
                    if stdout:
                        self.log_display.append(f"📄 Output: {stdout[:500]}...")
                    if stderr:
                        self.log_display.append(f"🚨 Error: {stderr[:500]}...")
                    self.log_display.append("💡 Use the Start button to try again manually")
                    # Reset the process reference
                    self.comfyui_process = None
                else:
                    self.log_display.append("✅ ComfyUI process running successfully")
                    
        except Exception as e:
            self.log_display.append(f"⚠️ Startup check error: {e}")
            
    def stop_comfyui(self):
        """Stop ComfyUI process"""
        try:
            processes = self.find_comfyui_processes()
            if not processes:
                QMessageBox.information(self, "Not Running", "ComfyUI is not running!")
                return
                
            # Graceful shutdown
            for proc_info in processes:
                try:
                    proc = psutil.Process(proc_info['pid'])
                    proc.terminate()
                    self.log_display.append(f"✅ Terminated process {proc_info['pid']}")
                except psutil.NoSuchProcess:
                    self.log_display.append(f"⚠️ Process {proc_info['pid']} already terminated")
                except Exception as e:
                    self.log_display.append(f"❌ Error terminating process {proc_info['pid']}: {e}")
                    
            self.status_bar.showMessage("Stopping ComfyUI...")
            self.log_display.append("🔄 ComfyUI stop requested")
            
        except Exception as e:
            error_msg = f"Failed to stop ComfyUI: {str(e)}"
            self.log_display.append(f"❌ {error_msg}")
            QMessageBox.critical(self, "Stop Error", error_msg)
            print(f"ComfyUI Manager - Stop Error: {e}")  # Debug output
            
    def restart_comfyui(self):
        """Restart ComfyUI"""
        try:
            self.log_display.append("🔄 Restarting ComfyUI...")
            self.stop_comfyui()
            QTimer.singleShot(2000, self.start_comfyui)  # Wait 2 seconds then start
        except Exception as e:
            error_msg = f"Failed to restart ComfyUI: {str(e)}"
            self.log_display.append(f"❌ {error_msg}")
            QMessageBox.critical(self, "Restart Error", error_msg)
            print(f"ComfyUI Manager - Restart Error: {e}")  # Debug output
        
    def kill_all_comfyui(self):
        """Force kill all ComfyUI processes"""
        reply = QMessageBox.question(
            self, "Kill All Processes",
            "This will forcefully terminate ALL ComfyUI processes!\n\nContinue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                processes = self.find_comfyui_processes()
                killed_count = 0
                
                for proc_info in processes:
                    try:
                        proc = psutil.Process(proc_info['pid'])
                        proc.kill()
                        killed_count += 1
                        self.log_display.append(f"Killed process {proc_info['pid']}")
                    except psutil.NoSuchProcess:
                        pass
                        
                QMessageBox.information(self, "Kill Complete", f"Killed {killed_count} processes")
                
            except Exception as e:
                QMessageBox.critical(self, "Kill Error", f"Failed to kill processes:\n{e}")
                
    def find_comfyui_processes(self) -> List[Dict]:
        """Find ComfyUI processes"""
        processes = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = ' '.join(proc.info['cmdline'] or [])
                    if any(keyword in cmdline.lower() for keyword in ['comfyui', 'main.py']):
                        if 'ComfyUI' in cmdline or 'main.py' in cmdline:
                            processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            print(f"Error finding processes: {e}")
        return processes
        
    def open_web_interface(self):
        """Open web interface in browser"""
        host = self.host_input.text()
        port = self.port_input.value()
        url = f"http://{host}:{port}"
        
        try:
            subprocess.Popen(['xdg-open', url])
            self.log_display.append(f"Opened web interface: {url}")
        except Exception as e:
            QMessageBox.critical(self, "Browser Error", f"Failed to open browser:\n{e}")
            
    def clear_logs(self):
        """Clear the log display"""
        self.log_display.clear()
        
    def refresh_logs(self):
        """Refresh log display"""
        # Could add real log file reading here
        pass
        
    def save_settings(self):
        """Save application settings"""
        self.settings.setValue("autostart", self.autostart_check.isChecked())
        self.settings.setValue("minimize_tray", self.minimize_tray_check.isChecked())
        self.settings.setValue("auto_browser", self.auto_open_browser_check.isChecked())
        self.settings.setValue("host", self.host_input.text())
        self.settings.setValue("port", self.port_input.value())
        
        QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully!")
        
    def load_settings(self):
        """Load application settings"""
        self.autostart_check.setChecked(self.settings.value("autostart", False, type=bool))
        self.minimize_tray_check.setChecked(self.settings.value("minimize_tray", True, type=bool))
        self.auto_open_browser_check.setChecked(self.settings.value("auto_browser", True, type=bool))
        self.host_input.setText(self.settings.value("host", "127.0.0.1", type=str))
        self.port_input.setValue(self.settings.value("port", 8188, type=int))
        
        # Auto-start if enabled
        if self.autostart_check.isChecked():
            QTimer.singleShot(1000, self.start_comfyui)
            
    def tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            
    def closeEvent(self, event):
        """Handle window close event"""
        if self.minimize_tray_check.isChecked() and QSystemTrayIcon.isSystemTrayAvailable():
            self.hide()
            event.ignore()
        else:
            self.quit_application()
            
    def quit_application(self):
        """Quit the application completely"""
        try:
            self.log_display.append("🔴 Manager shutting down...")
            
            # Stop ComfyUI first if running
            try:
                self.stop_comfyui()
            except Exception as e:
                print(f"Error stopping ComfyUI during quit: {e}")
            
            # Stop monitoring
            if hasattr(self, 'process_monitor'):
                self.process_monitor.stop()
                if self.process_monitor.isRunning():
                    self.process_monitor.wait(2000)  # Wait up to 2 seconds
                    if self.process_monitor.isRunning():
                        self.process_monitor.terminate()  # Force terminate if needed
                        
            # Stop update timer
            if hasattr(self, 'update_timer'):
                self.update_timer.stop()
                
        except Exception as e:
            print(f"Error during application quit: {e}")
        finally:
            QApplication.quit()


def handle_exception(exc_type, exc_value, exc_traceback):
    """Global exception handler to prevent unexpected crashes"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
        
    print(f"ComfyUI Manager - Unhandled exception: {exc_type.__name__}: {exc_value}")
    import traceback
    traceback.print_exception(exc_type, exc_value, exc_traceback)

def main():
    """Main application entry point"""
    # Set process name as early as possible (before Qt initialization)
    process_name = "ComfyUI-Manager"
    
    # Method 1: Override sys.argv[0] immediately
    sys.argv[0] = process_name
    
    # Method 2: Try to set process title via multiple approaches
    try:
        # Linux prctl method
        import ctypes
        import ctypes.util
        libc = ctypes.CDLL(ctypes.util.find_library("c"))
        PR_SET_NAME = 15
        libc.prctl(PR_SET_NAME, process_name.encode('utf-8'), 0, 0, 0)
        
        # Platform-independent setproctitle (if available)
        try:
            import setproctitle
            setproctitle.setproctitle(process_name)
        except ImportError:
            pass
            
        print(f"✅ Process name set to '{process_name}'")
    except Exception as e:
        print(f"⚠️ Process naming failed: {e}")
    
    # Install global exception handler
    sys.excepthook = handle_exception
    
    app = QApplication(sys.argv)
    
    # Set comprehensive application identification
    app.setApplicationName("ComfyUI Manager")
    app.setApplicationDisplayName("ComfyUI Manager")
    app.setApplicationVersion("2.0.9")
    app.setOrganizationName("ComfyUI")
    # Note: Removed setOrganizationDomain to prevent "org.comfyui.python3" process name
    app.setQuitOnLastWindowClosed(False)
    
    # Process name was set earlier in main() function
    
    # Set application icon
    app_dir = os.getenv('APPDIR', os.path.dirname(os.path.abspath(__file__)))
    icon_paths = [
        os.path.join(app_dir, 'comfyui.png'),
        os.path.join(app_dir, 'comfyui.svg'),
        os.path.join(os.path.dirname(__file__), 'comfyui.png'),
        os.path.join(os.path.dirname(__file__), 'comfyui.svg')
    ]
    
    app_icon = QIcon()
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app_icon = QIcon(icon_path)
            break
    
    app.setWindowIcon(app_icon)
    
    manager = ComfyUIManager()
    manager.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()