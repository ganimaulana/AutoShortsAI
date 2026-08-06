from __future__ import annotations
from application.scoring.decision_trace import DecisionTrace

class CandidateExplanationBuilder:
    """Converts a DecisionTrace into a human-readable explanation."""

    def build(self, trace: DecisionTrace) -> str:
        if not trace.steps:
            return "No decisions recorded."

        sections = []
        for step in trace.steps:
            section = [
                f"{step.stage}",
                "-" * 15
            ]
            
            # Format summaries
            if step.input_summary:
                for k, v in step.input_summary.items():
                    section.append(f"{k.replace('_', ' ').title()}: {v}")
            
            if step.explanation:
                section.append(step.explanation)
                
            # Specifically format summary keys if they exist
            if "bonus_count" in step.output_summary:
                section.append(f"Applied {step.output_summary['bonus_count']} bonus(es)")
            if "penalty_count" in step.output_summary:
                section.append(f"Applied {step.output_summary['penalty_count']} penalty(ies)")
            if "total_score" in step.output_summary:
                section.append(f"{step.output_summary['total_score']}")
                    
            sections.append("\n".join(section))
            
        return "\n\n↓\n\n".join(sections)
