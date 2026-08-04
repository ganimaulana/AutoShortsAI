from collections import deque

from domain.job.job import Job


class QueueManager:
    """
    FIFO Queue Manager.
    """

    def __init__(self):

        self._queue = deque()

    # -----------------------------------------

    def add(
        self,
        job: Job,
    ) -> None:

        self._queue.append(job)

    # -----------------------------------------

    def next(self) -> Job | None:
        """
        Ambil job berikutnya.
        """

        if not self._queue:
            return None

        return self._queue.popleft()

    # -----------------------------------------

    def pop(self) -> Job | None:
        """
        Alias next().
        """

        return self.next()

    # -----------------------------------------

    def peek(self) -> Job | None:

        if not self._queue:
            return None

        return self._queue[0]

    # -----------------------------------------

    def clear(self):

        self._queue.clear()

    # -----------------------------------------

    def is_empty(self) -> bool:

        return len(self._queue) == 0

    # -----------------------------------------

    def empty(self) -> bool:
        """
        Backward compatibility.
        """

        return self.is_empty()

    # -----------------------------------------

    def count(self) -> int:

        return len(self._queue)

    # -----------------------------------------

    def __len__(self):

        return len(self._queue)

    # -----------------------------------------

    def __iter__(self):

        return iter(self._queue)