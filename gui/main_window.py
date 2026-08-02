"""
==================================================
Naraseta Studio
AI Video Automation Platform

by Gani Creative Studio
==================================================
"""
import qtawesome as qta

from gui.widgets.log_console import LogConsole
from gui.widgets.progress_card import ProgressCard
from gui.widgets.thumbnail_widget import ThumbnailWidget
from gui.widgets.info_card import InfoCard

from PySide6.QtWidgets import (
    QHBoxLayout,
)
from gui.widgets.header import Header
from gui.widgets.url_card import UrlCard
from gui.widgets.card import Card

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
    QPushButton,
    QTextEdit,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QStatusBar,
    QSplitter,
    QFrame,
    QSizePolicy,

)


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.video_info = None
        self.current_url = ""
        self.thread = None
        self.worker = None

        self.project_path = None

        from gui.theme import APP_NAME, VERSION

        self.setWindowTitle(
            f"{APP_NAME} {VERSION}"
        )

        self.resize(
            1600,
            950,
        )

        self.build_ui()

    # ==================================================
    # UI
    # ==================================================

    def build_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        root = QVBoxLayout(central)

        self.root = root

        root.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        root.setSpacing(22)

        # -----------------------------------------
        # URL
        # -----------------------------------------

        header = Card()
        header.setMinimumHeight(120)
        header.setMaximumHeight(120)

        header.layout.addWidget(
            Header()
        )

        root.addWidget(
            header
        )

        # ============================
        # URL
        # ============================

        self.url_card = UrlCard()
        root.addWidget(self.url_card)

        # ============================
        # BUTTON
        # ============================

        button_layout = QHBoxLayout()

        button_layout.setSpacing(12)

        # ============================
        # BUTTON
        # ============================

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setIcon(
            qta.icon("fa5s.search", color="white")
        )
        self.analyze_button.clicked.connect(self.analyze_clicked)

        self.start_button = QPushButton("Start Pipeline")
        self.start_button.setIcon(
            qta.icon("fa5s.play", color="white")
        )
        self.start_button.clicked.connect(self.start_pipeline)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(
            qta.icon("fa5s.stop", color="white")
        )
        self.stop_button.clicked.connect(self.stop_pipeline)

        self.stop_button.setEnabled(False)

        self.analyze_button.setMinimumHeight(42)
        self.start_button.setMinimumHeight(42)
        self.stop_button.setMinimumHeight(42)

        self.analyze_button.setFixedSize(
            170,
            46,
        )

        self.start_button.setFixedSize(
            200,
            46,
        )

        self.stop_button.setFixedSize(
            150,
            46,
        )
        self.start_button.setMinimumWidth(180)
        self.stop_button.setMinimumWidth(140)

        button_layout.addWidget(self.analyze_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        button_layout.addStretch(1)

        root.addLayout(button_layout)

        # ======================================
        # PREVIEW AREA
        # ======================================

        preview_card = Card()

        preview_layout = QHBoxLayout()

        preview_layout.setContentsMargins(0,0,0,0)

        preview_layout.setSpacing(24)

        self.thumbnail = ThumbnailWidget()

        self.thumbnail.setFixedSize(
            360,
            202,
        )

        self.info_card = InfoCard()

        self.info_card.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Preferred,
        )

        preview_layout.addWidget(
            self.thumbnail
        )

        preview_layout.addWidget(
            self.info_card,
            1,
        )

        preview_card.layout.addLayout(
            preview_layout
        )

        root.addWidget(
            preview_card
        )
        # -----------------------------------------
        # Progress
        # -----------------------------------------

        self.progress_card = ProgressCard()
        self.progress_card.setMinimumHeight(170)

        root.addWidget(
            self.progress_card
        )     

        # -----------------------------------------
        # LOG
        # -----------------------------------------
        log_title = QLabel("🖥 System Console")

        log_title.setObjectName("CardTitle")

        root.addWidget(log_title)
        self.log_console = LogConsole()
        self.log_console.setMinimumHeight(260)

        root.addWidget(self.log_console)

        # -----------------------------------------
        # BOTTOM
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

        root.addLayout(bottom)

        # -----------------------------------------
        # STATUS BAR
        # -----------------------------------------

        self.status = QStatusBar()

        self.setStatusBar(self.status)

        self.status.showMessage(
            "Ready | Whisper | Ollama | Naraseta Studio"
        )

        # -----------------------------------------
        # MENU
        # -----------------------------------------

        about_action = QAction(
            "About",
            self,
        )

        menu = self.menuBar()

        help_menu = menu.addMenu("Help")

        help_menu.addAction(about_action)

        

    def write_log(self, message):

        self.log_console.append(
            message
        )

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

                self.progress_card.set_progress(value)

                self.progress_card.set_status(key)

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

            self.thumbnail.setPixmap(pixmap)

        except Exception:

            self.thumbnail.setText(
                "Thumbnail"
            )    

    # ==================================================
    # Analyze
    # ==================================================

    def analyze_clicked(self):

        url = self.url_card.text()
       

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
            self.progress_card.set_progress(0)



            self.status.showMessage(
                "Analyzing..."
            )

            self.progress_card.set_status(
                "Analyzing..."
            )
            
            self.write_log(
                "[INFO] Analyzing video..."
            )

            

            self.video_info = analyze_video(url)

            info = self.video_info

            metadata = {

                "title": info.get("title", "-"),

                "channel": info.get("uploader", "-"),

                "views_text": info.get("views_text", "-"),

                "duration_text": info.get("duration_text", "-"),

                "language": info.get("language", "-"),

                "upload_date": info.get("upload_date", "-"),

                "resolution": info.get("resolution", "-"),

            }

            self.info_card.update_info(
                metadata
            )
            self.load_thumbnail(
                info.get("thumbnail")
            )

        #    self.status_label.setText(
        #        "Ready to Start"
        #    )

            self.start_button.setEnabled(True)

            self.write_log(
                "[SUCCESS] Analyze completed."
            )

            self.progress_card.set_progress(100)

            self.status.showMessage(
                "Ready"
            )

            self.progress_card.set_status(
                "Ready"
            )


        except Exception as e:

            self.video_info = None
            self.current_url = ""

            self.progress_card.set_progress(0)

            self.info_card.update_info({})
            self.thumbnail.clear()

            self.thumbnail.setText(
                "No Thumbnail"
            )

        #    self.status_label.setText("Error")

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

            self.progress_card.set_status(
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

        self.progress_card.set_progress(0)

        self.start_button.setEnabled(False)

        self.stop_button.setEnabled(True)

        self.write_log(
            "[SYSTEM] Starting pipeline..."
        )

    #    self.status_label.setText(
    #        "Running"
    #    )

        self.status.showMessage(
            "Running"
        )

        self.progress_card.set_status(
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
        self.progress_card.set_progress(100)

        self.start_button.setEnabled(True)

        self.stop_button.setEnabled(False)

        self.status.showMessage(
            "Completed"
        )

        self.progress_card.set_status(
            "Completed"
        )

    #    self.status_label.setText(
    #        "Completed"
    #    )



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

            self.progress_card.set_status(
                "Cancelled"
            )

        #    self.status_label.setText(
        #        "Cancelled"
        #    )

            self.progress_card.set_progress(0)

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

        #    self.status_label.setText(
        #        "Error"
        #    )

            self.progress_card.set_progress(0)

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
