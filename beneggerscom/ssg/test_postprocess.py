from beneggerscom.ssg.postprocess import (
    add_footnote_class_to_footnote_paragraphs,
    move_footnotes_to_own_section,
)


def test_move_footnotes_to_own_section():
    html = """
<section>
<p>Some text</p>
<div class="footnote">
<p>Footnote text</p>
</div>
</section>
""".strip()
    expected = """
<section>
<p>Some text</p>
</section>
<div class="footnote">
<p>Footnote text</p>
</div>
""".strip()
    assert move_footnotes_to_own_section(html) == expected


def test_add_footnote_class_to_footnote_paragraphs():
    html = """
<p>
Some text[^1]
</p>
<p>
[^1]: Footnote text
</p>
""".strip()
    expected = """
<p>
Some text[^1]
</p>
<p class="footnote">
[^1]: Footnote text
</p>
""".strip()
    assert add_footnote_class_to_footnote_paragraphs(html) == expected
