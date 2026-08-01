import json


class PromptBuilder:

    @staticmethod
    def build(transcript):

        segments = []

        for seg in transcript:

            segments.append({

                "id": seg.id,

                "start": round(seg.start, 2),

                "end": round(seg.end, 2),

                "duration": round(seg.duration, 2),

                "text": seg.text.strip()

            })

        transcript_json = json.dumps(

            segments,

            ensure_ascii=False,

            indent=2

        )

        prompt = f"""
You are an expert YouTube Shorts editor.

Your job is to find the BEST viral moments.

Rules:

1. Use ONLY segment ids that already exist.
2. Never invent new ids.
3. Never invent timestamps.
4. Choose consecutive segments whenever possible.
5. Target clip duration between 20 and 60 seconds.
6. Return ONLY valid JSON.
7. No markdown.
8. No explanation.

JSON Format:

{{
  "clips":[
    {{
      "title":"...",
      "reason":"...",
      "segment_ids":[]
    }}
  ]
}}

Transcript:

{transcript_json}
"""

        return prompt