from domain.segment import Segment

from core.ai_engine import AIEngine


segments = [

    Segment(

        id=1,

        start=0,

        end=5,

        text="Halo semuanya.",

    ),

    Segment(

        id=2,

        start=5,

        end=12,

        text="Hari ini saya akan menceritakan kisah seorang pria.",

    ),

    Segment(

        id=3,

        start=12,

        end=23,

        text="Ia kehilangan seluruh hartanya dalam satu malam.",

    ),

    Segment(

        id=4,

        start=23,

        end=38,

        text="Namun akhirnya ia berhasil bangkit kembali.",

    )

]

engine = AIEngine()

timeline = engine.process(segments)

print()

print("=" * 60)
print("TIMELINE")
print("=" * 60)

for clip in timeline:

    print(clip)