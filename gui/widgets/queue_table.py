from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle


class QueueTable(Card):

    HEADERS = [

        "#",

        "Title",

        "Status",

        "Progress",

    ]

    def __init__(self):

        super().__init__()

        self.layout.addWidget(

            SectionTitle(

                "📋 Processing Queue"

            )

        )

        self.table = QTableWidget()

        self.table.setColumnCount(

            len(self.HEADERS)

        )

        self.table.setHorizontalHeaderLabels(

            self.HEADERS

        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            1,
            QHeaderView.Stretch,
        )

        self.table.setSelectionBehavior(

            QTableWidget.SelectRows

        )

        self.table.setEditTriggers(

            QTableWidget.NoEditTriggers

        )

        self.layout.addWidget(

            self.table

        )

    def add_job(
        self,
        job,
    ):

        row = self.table.rowCount()

        self.table.insertRow(row)

        #
        # Title
        #

        title = job.url

        metadata = getattr(job, "metadata", None)

        if isinstance(metadata, dict):

            title = metadata.get(
                "title",
                job.url,
            )

        #
        # Status
        #

        status = getattr(job, "status", None)

        if hasattr(status, "name"):

            status_text = status.name

        elif status is None:

            status_text = "Pending"

        else:

            status_text = str(status)

        #
        # Row
        #

        index_item = QTableWidgetItem(str(row + 1))
        index_item.setData(Qt.UserRole, job.id)

        self.table.setItem(
            row,
            0,
            index_item,
        )

        self.table.setItem(
            row,
            1,
            QTableWidgetItem(title),
        )

        self.table.setItem(
            row,
            2,
            QTableWidgetItem(status_text),
        )

        self.table.setItem(
            row,
            3,
            QTableWidgetItem("0%"),
        )

    def update_progress(

        self,

        row,

        percent,

    ):

        self.table.item(

            row,

            3,

        ).setText(

            f"{percent}%"

        )

    def update_status(

        self,

        row,

        status,

    ):

        self.table.item(

            row,

            2,

        ).setText(

            status

        )

    def update_job(self, job):

        for row in range(self.table.rowCount()):

            item = self.table.item(row, 0)

            if item is None:
                continue

            if item.data(Qt.UserRole) != job.id:
                continue

            status_text = getattr(job, "current_step", "")

            if not status_text:

                status = getattr(job, "status", None)

                if hasattr(status, "name"):
                    status_text = status.name
                else:
                    status_text = str(status)

            self.update_status(row, status_text.upper())

            progress = getattr(job, "progress", 0)

            self.update_progress(row, progress)

            return
