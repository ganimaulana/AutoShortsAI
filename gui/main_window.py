"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Main Window
==================================================
"""

from PySide6.QtCore import (
    Qt,
    QThread,
    QByteArray,
)

from PySide6.QtGui import (
    QAction,
    QPixmap,
)

from core.analyzer import analyze_video
from pathlib import Path
import os

from gui.worker import PipelineWorker
from urllib.request import urlopen

from PySide6.QtWidgets import (
    QMessageBox,
    QMainWindow,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QTextEdit,
    QProgressBar,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QFormLayout,
    QStatusBar,
)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.video_info = None
        self.current_url = ""
        self.thread = None
        self.worker = None

        self.project_path = None

        self.setWindowTitle("AutoShortsAI v0.1")

        self.resize(1200, 800)

        self.build_ui()

    # ==================================================
    # UI
    # ==================================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        root.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        root.setSpacing(15)

        # -----------------------------------------
        # URL
        # -----------------------------------------

        url_group = QGroupBox("YouTube URL")

        url_layout = QVBoxLayout(url_group)

        self.url_edit = QLineEdit()

        self.url_edit.setPlaceholderText(
            "https://youtube.com/watch?v=..."
        )

        url_layout.addWidget(
            self.url_edit
        )

        button_layout = QHBoxLayout()

        self.analyze_button = QPushButton(
            "Analyze"
        )

        self.analyze_button.clicked.connect(
            self.analyze_clicked
        )

        self.start_button = QPushButton(
            "Start"
        )

        self.start_button.clicked.connect(
            self.start_pipeline
        )

        self.start_button.setEnabled(False)

        self.stop_button = QPushButton(
            "Stop"
        )

        self.stop_button.setEnabled(False)

        self.stop_button.clicked.connect(
            self.stop_pipeline
        )

        button_layout.addWidget(
            self.analyze_button
        )

        button_layout.addWidget(
            self.start_button
        )

        button_layout.addWidget(
            self.stop_button
        )

        button_layout.addStretch()

        url_layout.addLayout(
            button_layout
        )

        root.addWidget(
            url_group
        )

        # -----------------------------------------
        # Project
        # -----------------------------------------

        project_group = QGroupBox(
            "Project Information"
        )

        project_layout = QHBoxLayout(
            project_group
        )

        #
        # Thumbnail
        #

        self.thumbnail = QLabel(
            "Thumbnail"
        )

        self.thumbnail.setAlignment(
            Qt.AlignCenter
        )

        self.thumbnail.setFixedSize(
            220,
            124,
        )

        self.thumbnail.setStyleSheet(
            """
            background:#3b3b3b;
            border:1px solid gray;
            border-radius:6px;
            """
        )

        project_layout.addWidget(
            self.thumbnail
        )

        #
        # Metadata
        #

        form = QFormLayout()

        self.title_label = QLabel("-")

        self.channel_label = QLabel("-")

        self.duration_label = QLabel("-")

        self.language_label = QLabel("-")

        self.status_label = QLabel(
            "Ready"
        )

        form.addRow(
            "Title",
            self.title_label,
        )

        form.addRow(
            "Channel",
            self.channel_label,
        )

        form.addRow(
            "Duration",
            self.duration_label,
        )

        form.addRow(
            "Language",
            self.language_label,
        )

        form.addRow(
            "Status",
            self.status_label,
        )

        project_layout.addLayout(
            form
        )

        root.addWidget(
            project_group
        )

        # -----------------------------------------
        # Progress
        # -----------------------------------------

        progress_group = QGroupBox(
            "Progress"
        )

        progress_layout = QVBoxLayout(
            progress_group
        )

        self.progress = QProgressBar()

        self.progress.setRange(
            0,
            100,
        )

        
        self.progress.setValue(
            0
        )

        progress_layout.addWidget(
            self.progress
        )

        root.addWidget(
            progress_group
        )


        # -----------------------------------------
        # Log
        # -----------------------------------------

        log_group = QGroupBox(
            "Log"
        )

        log_layout = QVBoxLayout(
            log_group
        )

        self.log = QTextEdit()

        self.log.setReadOnly(True)

        log_layout.addWidget(
            self.log
        )

        self.write_log(
            "[SYSTEM] Welcome to AutoShortsAI"
        )

        self.write_log(
            "[SYSTEM] Ready."
        )

        

        root.addWidget(
            log_group
        )

        # -----------------------------------------
        # Bottom
        # -----------------------------------------

        bottom = QHBoxLayout()

        bottom.addStretch()

        self.open_project_button = QPushButton(
            "Open Project Folder"
        )

        self.open_project_button.clicked.connect(
            self.open_project_folder
        )

        bottom.addWidget(
            self.open_project_button
        )

        root.addLayout(
            bottom
        )

        # -----------------------------------------
        # Status Bar
        # -----------------------------------------

        self.status = QStatusBar()

        self.setStatusBar(
            self.status
        )

        self.status.showMessage(
            "Ready"
        )

        # -----------------------------------------
        # Menu
        # -----------------------------------------

        about_action = QAction(
            "About",
            self,
        )

        menu = self.menuBar()

        help_menu = menu.addMenu(
            "Help"
        )

        help_menu.addAction(
            about_action
        )
    
    # ==================================================
    # Log
    # ==================================================

    def write_log(self, message):

        self.log.append(message)

        self.log.ensureCursorVisible()

        progress_map = {

            "Analyzing": 10,

            "Creating project": 15,

            "Downloading": 25,

            "Transcribing": 40,

            "Building stories": 55,

            "Ranking stories": 65,

            "Building timeline": 75,

            "Generating clips": 90,

            "Rendering subtitles": 98,

            "Completed": 100,

        }

        for key, value in progress_map.items():

            if key in message:

                self.progress.setValue(value)

                break
    # ==================================================
    # Thumbnail
    # ==================================================

    def load_thumbnail(self, url):

        if not url:
            return

        try:

            data = urlopen(url).read()

            pixmap = QPixmap()

            pixmap.loadFromData(
                QByteArray(data)
            )

            self.thumbnail.setPixmap(

                pixmap.scaled(

                    self.thumbnail.size(),

                    Qt.KeepAspectRatio,

                    Qt.SmoothTransformation,

                )

            )

        except Exception:

            self.thumbnail.setText(
                "Thumbnail"
            )    

    # ==================================================
    # Analyze
    # ==================================================

    def analyze_clicked(self):

        url = self.url_edit.text().strip()
       

        if not url:

            QMessageBox.warning(
                self,
                "URL",
                "Please enter YouTube URL."
            )

            return

        self.current_url = url

        try:

            self.analyze_button.setEnabled(False)
            self.progress.setValue(0)



            self.status.showMessage(
                "Analyzing..."
            )

            self.write_log(
                "[INFO] Analyzing video..."
            )

            

            self.video_info = analyze_video(url)

            info = self.video_info

            self.title_label.setText(
                info.get("title", "-")
            )

            self.channel_label.setText(
                info.get("uploader", "-")
            )

            self.duration_label.setText(
                str(info.get("duration", "-"))
            )

            self.language_label.setText(
                info.get("language", "-")
            )

            self.load_thumbnail(
                info.get("thumbnail")
            )

            self.status_label.setText(
                "Ready to Start"
            )

            self.start_button.setEnabled(True)

            self.write_log(
                "[SUCCESS] Analyze completed."
            )

            self.progress.setValue(100)

            self.status.showMessage(
                "Ready"
            )


        except Exception as e:

            self.video_info = None
            self.current_url = ""

            self.progress.setValue(0)

            self.title_label.setText("-")
            self.channel_label.setText("-")
            self.duration_label.setText("-")
            self.language_label.setText("-")
            self.thumbnail.clear()

            self.thumbnail.setText(
                "Thumbnail"
            )

            self.status_label.setText("Error")

            self.start_button.setEnabled(False)


            QMessageBox.critical(
                self,
                "Error",
                str(e)
            )

            self.write_log(
                f"[ERROR] {e}"
            )

            self.status.showMessage(
                "Error"
            )

        finally:

            self.analyze_button.setEnabled(True)

    # ==================================================
    # Start Pipeline
    # ==================================================

    def start_pipeline(self):

        if self.thread is not None:

            return

        if not self.current_url:

            return

        self.progress.setValue(0)

        self.start_button.setEnabled(False)

        self.stop_button.setEnabled(True)

        self.write_log(
            "[SYSTEM] Starting pipeline..."
        )

        self.status_label.setText(
            "Running"
        )

        self.status.showMessage(
            "Running"
        )

        #
        # Thread
        #

        self.thread = QThread()

        self.worker = PipelineWorker(
            self.current_url
        )

        self.worker.moveToThread(
            self.thread
        )

        #
        # Connections
        #

        self.thread.started.connect(
            self.worker.run
        )

        self.worker.log.connect(
            self.write_log
        )

        self.worker.finished.connect(
            self.pipeline_finished
        )

        self.worker.error.connect(
            self.pipeline_error
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.worker.deleteLater
        )

        #
        # Cleanup
        #

        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            lambda: setattr(
                self,
                "thread",
                None,
            )
        )

        self.thread.finished.connect(
            lambda: setattr(
                self,
                "worker",
                None,
            )
        )

        self.thread.start()

    # ==================================================
    # Pipeline Finished
    # ==================================================

    def pipeline_finished(self, context):

        self.write_log(
            "[SUCCESS] Pipeline completed."
        )

        self.project_path = context.project_path
        self.progress.setValue(100)

        self.start_button.setEnabled(True)

        self.stop_button.setEnabled(False)

        self.status.showMessage(
            "Completed"
        )

        self.status_label.setText(
            "Completed"
        )



        # ==================================================
        # Pipeline Error
        # ==================================================

    def pipeline_error(self, message):

        self.start_button.setEnabled(True)

        self.stop_button.setEnabled(False)

        if "Pipeline cancelled" in message:

            self.write_log(
                "[SYSTEM] Pipeline cancelled."
            )

            self.status.showMessage(
                "Cancelled"
            )

            self.status_label.setText(
                "Cancelled"
            )

            self.progress.setValue(0)

        else:

            QMessageBox.critical(
                self,
                "Pipeline Error",
                message
            )

            self.write_log(
                f"[ERROR] {message}"
            )

            self.status.showMessage(
                "Error"
            )

            self.status_label.setText(
                "Error"
            )

            self.progress.setValue(0)

        self.thread = None

        self.worker = None

    # ==================================================
    # Open Project Folder
    # ==================================================

    def open_project_folder(self):

        if not self.project_path:

            QMessageBox.information(
                self,
                "Project",
                "No project available."
            )

            return

        path = Path(self.project_path)

        if not path.exists():

            QMessageBox.warning(
                self,
                "Project",
                "Project folder not found."
            )

            return

        os.startfile(path)
    # ==================================================
    # Stop Pipeline
    # ==================================================

    def stop_pipeline(self):

        if self.worker is None:

            return

        self.write_log(
            "[SYSTEM] Cancelling pipeline..."
        )

        self.worker.cancel()

        self.stop_button.setEnabled(False)

        self.status.showMessage(
            "Cancelling..."
        )
