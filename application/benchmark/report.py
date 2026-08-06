from __future__ import annotations
from application.benchmark.runner import BenchmarkResult

class BenchmarkReporter:
    @staticmethod
    def report(name: str, result: BenchmarkResult) -> str:
        return f"Benchmark: {name}\nPrecision@K: {result.precision_at_k:.2f}\nRecall@K: {result.recall_at_k:.2f}"
