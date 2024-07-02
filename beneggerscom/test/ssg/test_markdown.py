from beneggerscom.ssg.markdown import (
    _process_bolds,
    _process_headings,
    _process_italics,
    _process_links,
)


def test_process_headings_no_headings():
    assert _process_headings("No headings here") == "No headings here"


def test_process_headings_one_heading_one():
    assert _process_headings("# Heading 1") == "<h1>Heading 1</h1>"


def test_process_headings_one_heading_two():
    assert _process_headings("## Heading 2") == "<h2>Heading 2</h2>"


def test_process_headings_one_heading_three():
    assert _process_headings("### Heading 3") == "<h3>Heading 3</h3>"


def test_process_headings_one_heading_four():
    assert _process_headings("#### Heading 4") == "<h4>Heading 4</h4>"


def test_process_headings_one_heading_five():
    assert _process_headings("##### Heading 5") == "<h5>Heading 5</h5>"


def test_process_one_heading_plus_text():
    text = """
# Heading 1
Some text
"""
    expected = """
<h1>Heading 1</h1>
Some text
"""
    assert _process_headings(text) == expected


def test_process_one_heading_after_text():
    text = """
Some text
# Heading 1
"""
    expected = """
Some text
<h1>Heading 1</h1>
"""
    assert _process_headings(text) == expected


def test_process_headings_multiple_headings():
    text = """
# Heading 1

Text

## Heading 2

More text

### Heading 3
"""
    expected = """
<h1>Heading 1</h1>

Text

<h2>Heading 2</h2>

More text

<h3>Heading 3</h3>
"""
    assert _process_headings(text) == expected


def test_bold_no_bold():
    assert _process_bolds("No bold here") == "No bold here"


def test_bold_asterisks_one_bold():
    assert _process_bolds("**Bold text**") == "<strong>Bold text</strong>"


def test_bold_asterisks_one_bold_plus_text():
    text = """
**Bold text**
Non-bold text
"""
    expected = """
<strong>Bold text</strong>
Non-bold text
"""
    assert _process_bolds(text) == expected


def test_bold_asterisks_one_bold_after_text():
    text = """
Non-bold text
**Bold text**
"""
    expected = """
Non-bold text
<strong>Bold text</strong>
"""
    assert _process_bolds(text) == expected


def test_bold_asterisks_multiple_bold():
    text = """
**Bold 1**
Non-bold text
**Bold 2**
"""
    expected = """
<strong>Bold 1</strong>
Non-bold text
<strong>Bold 2</strong>
"""
    assert _process_bolds(text) == expected


def test_bold_underscores_one_bold():
    assert _process_bolds("__Bold text__") == "<strong>Bold text</strong>"


def test_bold_underscores_one_bold_plus_text():
    text = """
__Bold text__
Non-bold text
"""
    expected = """
<strong>Bold text</strong>
Non-bold text
"""
    assert _process_bolds(text) == expected


def test_bold_underscores_one_bold_after_text():
    text = """
Non-bold text
__Bold text__
"""
    expected = """
Non-bold text
<strong>Bold text</strong>
"""
    assert _process_bolds(text) == expected


def test_bold_underscores_multiple_bold():
    text = """
__Bold 1__
Non-bold text
__Bold 2__
"""
    expected = """
<strong>Bold 1</strong>
Non-bold text
<strong>Bold 2</strong>
"""
    assert _process_bolds(text) == expected


def test_italics_no_italics():
    assert _process_italics("No italics here") == "No italics here"


def test_italics_asterisks_one_italics():
    assert _process_italics("*Italic text*") == "<em>Italic text</em>"


def test_italics_asterisks_one_italics_plus_text():
    text = """
*Italic text*
Non-italic text
"""
    expected = """
<em>Italic text</em>
Non-italic text
"""
    assert _process_italics(text) == expected


def test_italics_asterisks_one_italics_after_text():
    text = """
Non-italic text
*Italic text*
"""
    expected = """
Non-italic text
<em>Italic text</em>
"""
    assert _process_italics(text) == expected


def test_italics_asterisks_multiple_italics():
    text = """
*Italic 1*
Non-italic text
*Italic 2*
"""
    expected = """
<em>Italic 1</em>
Non-italic text
<em>Italic 2</em>
"""
    assert _process_italics(text) == expected


def test_italics_underscores_one_italics():
    assert _process_italics("_Italic text_") == "<em>Italic text</em>"


def test_italics_underscores_one_italics_plus_text():
    text = """
_Italic text_
Non-italic text
"""
    expected = """
<em>Italic text</em>
Non-italic text
"""
    assert _process_italics(text) == expected


def test_italics_underscores_one_italics_after_text():
    text = """
Non-italic text
_Italic text_
"""
    expected = """
Non-italic text
<em>Italic text</em>
"""
    assert _process_italics(text) == expected


def test_italics_underscores_multiple_italics():
    text = """
_Italic 1_
Non-italic text
_Italic 2_
"""
    expected = """
<em>Italic 1</em>
Non-italic text
<em>Italic 2</em>
"""
    assert _process_italics(text) == expected


def test_links_no_links():
    assert _process_links("No links here") == "No links here"


def test_links_one_link():
    assert _process_links("[Link](https://example.com)") == \
        '<a href="https://example.com">Link</a>'


def test_links_one_link_plus_text():
    text = """
[Link](https://example.com)
Non-link text
"""
    expected = """
<a href="https://example.com">Link</a>
Non-link text
"""
    assert _process_links(text) == expected


def test_links_one_link_after_text():
    text = """
Non-link text
[Link](https://example.com)
"""
    expected = """
Non-link text
<a href="https://example.com">Link</a>
"""
    assert _process_links(text) == expected


def test_links_multiple_links():
    text = """
[Link 1](https://example.com)
Non-link text
[Link 2](https://example.com)
"""
    expected = """
<a href="https://example.com">Link 1</a>
Non-link text
<a href="https://example.com">Link 2</a>
"""
    assert _process_links(text) == expected
