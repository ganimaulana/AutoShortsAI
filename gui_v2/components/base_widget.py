"""
==========================================================
Base Widget

Semua widget pada GUI V2 mewarisi class ini.

Author : Gani Creative Studio
==========================================================
"""

from __future__ import annotations

from PySide6.QtWidgets import QWidget


class BaseWidget(QWidget):
    """
    Base class untuk seluruh widget.

    Lifecycle:
        __init__()
            ↓
        build_ui()
            ↓
        connect_signal()
            ↓
        update_state()
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.build_ui()
        self.connect_signal()

    # --------------------------------------------------

    def build_ui(self):
        """Bangun seluruh UI"""
        pass

    # --------------------------------------------------

    def connect_signal(self):
        """Hubungkan signal-slot"""
        pass

    # --------------------------------------------------

    def update_state(self):
        """Refresh tampilan"""
        pass

    # --------------------------------------------------

    def clear(self):
        """Reset widget"""
        pass