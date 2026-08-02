from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from domain.job.manifest import Manifest
from domain.job.status import JobStatus


@dataclass(slots=True)
class Job:
    """
    Merepresentasikan satu proses penuh dari:
    YouTube URL -> Download -> AI -> Render -> Upload
    """

    # ==========================
    # Identity
    # ==========================
    id: str = field(default_factory=lambda: uuid4().hex[:8])

    url: str = ""

    workspace: Path = Path()

    created_at: datetime = field(default_factory=datetime.now)

    # ==========================
    # Runtime
    # ==========================
    status: JobStatus = JobStatus.PENDING

    progress: int = 0

    current_step: str = ""

    error_message: str = ""

    cancelled: bool = False

    # ==========================
    # Data
    # ==========================
    manifest: Manifest = field(default_factory=Manifest)

    metadata: dict = field(default_factory=dict)

    # ==========================
    # Helper
    # ==========================

    def update_status(
        self,
        status: JobStatus,
        step: str = "",
    ) -> None:

        self.status = status

        self.current_step = step

    def update_progress(
        self,
        progress: int,
    ) -> None:

        progress = max(0, min(100, progress))

        self.progress = progress

    def fail(
        self,
        message: str,
    ) -> None:

        self.status = JobStatus.FAILED

        self.error_message = message

    def complete(self) -> None:

        self.status = JobStatus.COMPLETED

        self.progress = 100

    def cancel(self) -> None:

        self.cancelled = True

        self.status = JobStatus.CANCELLED

    @property
    def is_finished(self) -> bool:

        return self.status in (

            JobStatus.COMPLETED,

            JobStatus.FAILED,

            JobStatus.CANCELLED,

        )

    @property
    def is_running(self) -> bool:

        return not self.is_finished