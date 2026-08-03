from dataclasses import dataclass, field

from domain.transcript.models import Transcript
from domain.clip.models import ClipCandidate
from domain.render.render_plan import RenderPlan


@dataclass(slots=True)
class JobContext:

    transcript: Transcript | None = None

    candidates: list[ClipCandidate] = field(
        default_factory=list
    )

    approved_candidates: list[
        ClipCandidate
    ] = field(default_factory=list)

    render_plans: list[
        RenderPlan
    ] = field(default_factory=list)