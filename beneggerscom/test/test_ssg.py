from beneggerscom.ssg.postprocess import move_footnotes_to_own_section


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
