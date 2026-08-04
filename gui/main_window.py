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
from PySide6.QtCore import QThread
from gui.widgets.queue_table import QueueTable
from pathlib import Path
from datetime import datetime
import re

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

        #
        # Queue
        #
        from application.queue_manager import QueueManager

        self.queue = QueueManager()

        #
        # Worker
        #
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

        #
        # Analyze
        #

        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.setIcon(
            qta.icon(
                "fa5s.search",
                color="white",
            )
        )

        self.analyze_button.clicked.connect(
            self.analyze_clicked
        )

        #
        # Add Queue
        #

        self.add_queue_button = QPushButton(
            "Add Queue"
        )

        self.add_queue_button.setIcon(

            qta.icon(

                "fa5s.plus",

                color="white",

            )

        )

        self.add_queue_button.clicked.connect(

            self.add_queue_clicked

        )

        self.add_queue_button.setEnabled(
            False
        )

        #
        # Start Queue
        #

        self.start_button = QPushButton(
            "Start Queue"
        )

        self.start_button.setIcon(

            qta.icon(

                "fa5s.play",

                color="white",

            )

        )

        self.start_button.clicked.connect(

            self.start_queue

        )

        self.start_button.setEnabled(
            False
        )

        #
        # Stop
        #

        self.stop_button = QPushButton(
            "Stop"
        )

        self.stop_button.setIcon(

            qta.icon(

                "fa5s.stop",

                color="white",

            )

        )

        self.stop_button.clicked.connect(

            self.stop_pipeline

        )

        self.stop_button.setEnabled(
            False
        )

        #
        # Size
        #

        for button in (

            self.analyze_button,

            self.add_queue_button,

            self.start_button,

            self.stop_button,

        ):

            button.setFixedHeight(46)

        button_layout.addWidget(
            self.analyze_button
        )

        button_layout.addWidget(
            self.add_queue_button
        )

        button_layout.addWidget(
            self.start_button
        )

        button_layout.addWidget(
            self.stop_button
        )

        button_layout.addStretch()

        root.addLayout(
            button_layout
        )

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
        # LOG + QUEUE
        # -----------------------------------------

        bottom_panel = QHBoxLayout()

        self.log_console = LogConsole()
        self.log_console.setMinimumHeight(260)

        self.queue_table = QueueTable()
        self.queue_table.setMinimumHeight(260)

        bottom_panel.addWidget(
            self.log_console,
            2,          # 2/3 lebar
        )

        bottom_panel.addWidget(
            self.queue_table,
            1,          # 1/3 lebar
        )

        root.addLayout(bottom_panel)
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

        level = "INFO"

        upper = message.upper()

        if "[ERROR]" in upper:
            level = "ERROR"
        elif "[SUCCESS]" in upper:
            level = "SUCCESS"
        elif "[WARNING]" in upper:
            level = "WARNING"

        self.log_console.log(
            message,
            level,
        )

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

            from domain.job.job import Job

            title = self.video_info.get(
                "title",
                "Untitled",
            )

            safe_title = re.sub(
                r'[<>:"/\\|?*]',
                "",
                title,
            ).strip()

            safe_title = safe_title.replace(
                " ",
                "_",
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            workspace = (
                Path.cwd()
                / "projects"
                / f"{timestamp}_{safe_title}"
            )

            workspace.mkdir(
                parents=True,
                exist_ok=True,
            )

            for folder in (
                "input",
                "output",
                "subtitle",
                "transcript",
                "temp",
            ):
                (workspace / folder).mkdir(
                    exist_ok=True,
                )

            print("=" * 60)
            print("WORKSPACE :", workspace)
            print("EXISTS    :", workspace.exists())

            import os

            print("LISTDIR   :", os.listdir(workspace))

            print("INPUT     :", (workspace / "input").exists())
            print("OUTPUT    :", (workspace / "output").exists())
            print("=" * 60)

            print("WORKSPACE =", workspace)

            self.pending_job = Job(
                url=url,
                workspace=workspace,
            )

            print("Workspace exists :", workspace.exists())
            print("Input exists     :", (workspace / "input").exists())
            print("Workspace path   :", workspace)

            self.project_path = str(workspace)
            self.pending_job.metadata = self.video_info

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

            self.add_queue_button.setEnabled(True)
            self.start_button.setEnabled(False)

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

        #
        # Thread masih berjalan
        #
        if self.thread is not None:
            return

        #
        # Pastikan ada current job
        #
        if not hasattr(self, "current_job") or self.current_job is None:

            QMessageBox.warning(
                self,
                "Queue",
                "Tidak ada job yang akan diproses."
            )

            return

        #
        # Update UI
        #
        self.pipeline_progress(0, "PENDING")

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.write_log(
            "[SYSTEM] Starting pipeline..."
        )

        #
        # Worker
        #
        self.thread = QThread()

        self.worker = PipelineWorker(
            self.current_job
        )

        self.worker.moveToThread(
            self.thread
        )

        #
        # Thread Start
        #
        self.thread.started.connect(
            self.worker.run
        )

        #
        # Worker Signals
        #
        self.worker.log.connect(
            self.write_log
        )

        self.worker.progress.connect(
            self.pipeline_progress
        )

        self.worker.finished.connect(
            self.pipeline_finished
        )

        self.worker.error.connect(
            self.pipeline_error
        )

        #
        # Cleanup
        #
        self.worker.finished.connect(
            self.thread.quit
        )

        self.worker.error.connect(
            self.thread.quit
        )

        self.worker.finished.connect(
            self.worker.deleteLater
        )

        self.worker.error.connect(
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

        #
        # Start
        #
        self.thread.start()

    # ==================================================
    # Pipeline Finished
    # ==================================================

    def pipeline_finished(self, job):

        self.project_path = str(job.workspace)

        #
        # Pastikan UI berada pada state terakhir
        #
        self.pipeline_progress(
            100,
            "COMPLETED",
        )

        #
        # Tambahkan log yang hilang
        #
        self.write_log(
            "[Render] Finished"
        )

        self.write_log(
            "[SUCCESS] Pipeline Completed"
        )

        #
        # Tombol
        #
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)


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

            self.pipeline_progress(0, "CANCELLED")

        else:

            print(message)

            QMessageBox.critical(
                self,
                "Pipeline Error",
                message
            )

            self.write_log(
                f"[ERROR] {message}"
            )

            self.pipeline_progress(0, "ERROR")

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

        self.pipeline_progress(
            self.current_job.progress,
            "CANCELLING",
        )

    def add_queue_clicked(self):

        print("DEBUG 1 - add_queue_clicked")

        if not hasattr(self, "pending_job"):
            QMessageBox.warning(
                self,
                "Queue",
                "Analyze video terlebih dahulu.",
            )
            return

        self.queue.add(self.pending_job)

        print("========== ADD QUEUE ==========")
        print("Queue object id :", id(self.queue))
        print("Queue length    :", len(self.queue))
        print("Queue empty     :", self.queue.is_empty())

        print("DEBUG 2 - queue size:", len(self.queue))

        self.queue_table.add_job(self.pending_job)

        self.start_button.setEnabled(True)

        print("DEBUG 3 - start enabled:", self.start_button.isEnabled())

        self.add_queue_button.setEnabled(False)

        self.write_log("[QUEUE] Added.")
        
    def start_queue(self):

        print("========== START QUEUE ==========")
        print("Queue object id :", id(self.queue))
        print("Queue length    :", len(self.queue))
        print("Queue empty     :", self.queue.is_empty())

        if not self.queue.is_empty():
            print("Next job peek   :", self.queue.peek())

        if self.queue.is_empty():

            QMessageBox.information(
                self,
                "Queue",
                "Queue kosong."
            )
            return

        self.current_job = self.queue.next()

        print("Current job :", self.current_job)

        self.start_pipeline()

    def pipeline_progress(self, percent, stage):

        stage = stage.upper()

        self.progress_card.set_progress(percent)

        self.progress_card.set_status(stage)

        self.status.showMessage(
            f"{stage} | {percent}%"
        )

        if hasattr(self, "current_job"):

            #
            # Progress
            #
            self.current_job.progress = percent

            #
            # Current Step
            #
           
            self.current_job.current_step = stage
  

            #
            # >>> TAMBAHKAN BAGIAN INI <<<
            #
            

            #
            # Refresh Queue
            #
            try:
                self.queue_table.update_job(self.current_job)
            except Exception:
                pass
