from collections import deque

from domain.job.job import Job


class QueueManager:

    def __init__(self):

        self.queue = deque()

    def add(
        self,
        job: Job,
    ):

        self.queue.append(job)

    def pop(self):

        if not self.queue:

            return None

        return self.queue.popleft()

    def clear(self):

        self.queue.clear()

    def __len__(self):

        return len(self.queue)

    def empty(self):

        return len(self.queue) == 0