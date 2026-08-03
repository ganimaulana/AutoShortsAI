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

        self.table.setItem(

            row,

            0,

            QTableWidgetItem(

                str(row + 1)

            ),

        )

        self.table.setItem(

            row,

            1,

            QTableWidgetItem(

                job.video.title

            ),

        )

        self.table.setItem(

            row,

            2,

            QTableWidgetItem(

                job.status.name

            ),

        )

        self.table.setItem(

            row,

            3,

            QTableWidgetItem(

                "0%"

            ),

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