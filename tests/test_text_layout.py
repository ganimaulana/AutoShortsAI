from media.text_layout import TextLayout


def test_layout():

    layout = TextLayout()

    text = (
        "Indonesia tidak pernah dijajah Belanda "
        "karena sebenarnya VOC bukan negara."
    )

    result = layout.wrap(text)

    print()

    print("=" * 60)

    print("Text Layout")

    print("=" * 60)

    for line in result:

        print(line)

    print("=" * 60)

    assert len(result) <= 2