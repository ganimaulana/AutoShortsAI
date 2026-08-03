from pipeline.runner import PipelineRunner

from pipeline.analyze_pipeline import AnalyzePipeline
from pipeline.download_pipeline import DownloadPipeline
from pipeline.whisper_pipeline import WhisperPipeline
from pipeline.render_pipeline import RenderPipeline


def run_pipeline(
    job,
    progress_callback=None,
    log_callback=None,
    cancel_callback=None,
):
    """
    Adapter agar Worker lama tetap bisa
    menggunakan PipelineRunner baru.
    """

    runner = PipelineRunner(
        [
            AnalyzePipeline(),
            DownloadPipeline(),
            WhisperPipeline(),
            RenderPipeline(),
        ],
        progress_callback=progress_callback,
        log_callback=log_callback,
        cancel_callback=cancel_callback,
    )

    return runner.run(job)