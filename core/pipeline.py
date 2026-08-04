from pipeline.analyze_pipeline import AnalyzePipeline
from pipeline.base_pipeline import PipelineStep
from pipeline.download_pipeline import DownloadPipeline
from pipeline.runner import PipelineRunner
from pipeline.whisper_pipeline import WhisperPipeline
from pipeline.render_pipeline import RenderPipeline


def build_pipeline_runner(
    progress_callback=None,
    log_callback=None,
    cancel_callback=None,
) -> PipelineRunner:
    """Create the single active, Job-based pipeline runner.

    The stage order is deliberately unchanged for Migration Phase 1.
    """

    runner = PipelineRunner(
        progress_callback=progress_callback,
        log_callback=log_callback,
        cancel_callback=cancel_callback,
    )

    steps: tuple[PipelineStep, ...] = (
        AnalyzePipeline(),
        DownloadPipeline(),
        WhisperPipeline(),
        RenderPipeline(),
    )

    for step in steps:

        runner.add_step(step)

    return runner


def run_pipeline(
    job,
    progress_callback=None,
    log_callback=None,
    cancel_callback=None,
):
    """
    Entry point pipeline.
    """
    print("=" * 60)
    print("RUN_PIPELINE CALLED")
    print("JOB =", job)
    print("WORKSPACE =", job.workspace)
    print("=" * 60)
    
    return build_pipeline_runner(
        progress_callback=progress_callback,
        log_callback=log_callback,
        cancel_callback=cancel_callback,
    ).run(job)
