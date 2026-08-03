from abc import ABC
from abc import abstractmethod


class PipelineStep(ABC):

    name = "Unnamed"

    @abstractmethod

    def execute(

        self,

        job,

        context,

    ):

        pass