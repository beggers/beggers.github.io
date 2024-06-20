from beneggerscom.ssg.markdown import _process_bolds, _process_headings


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
