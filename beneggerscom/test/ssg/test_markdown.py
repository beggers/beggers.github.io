from beneggerscom.ssg.markdown import (
    _process_bolds,
    _process_headings,
    _process_italics,
    _process_links,
    _process_paragraphs_and_lists,
)


def equals_ignore_whitespace(a: str, b: str) -> bool:
    return "".join(a.split()) == "".join(b.split())


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


def test_paragraphs_single_line():
    text = "Just a single line of text"
    expected = "<p>Just a single line of text</p>"
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_paragraphs_multiple_paragraphs():
    text = """Line one
Line two

Line three

Line four and five
Line five continued"""
    expected = """<p>Line one Line two</p>
<p>Line three</p>
<p>Line four and five Line five continued</p>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_unordered_list_simple():
    text = """- Item one
- Item two
- Item three"""
    expected = """<ul>
<li><p>Item one</p></li>
<li><p>Item two</p></li>
<li><p>Item three</p></li>
</ul>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_ordered_list_simple():
    text = """1. First item
2. Second item
3. Third item"""
    expected = """<ol>
<li><p>First item</p></li>
<li><p>Second item</p></li>
<li><p>Third item</p></li>
</ol>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_unordered_list_multiple_paragraphs_in_item():
    text = """- First item line one

  First item line two

  First item line three
- Second item"""
    expected = """<ul>
<li><p>First item line one</p>
<p>First item line two</p>
<p>First item line three</p></li>
<li><p>Second item</p></li>
</ul>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_paragraphs_multiple_lines_one_paragraph():
    text = """Line one
Line two
Line three"""
    expected = "<p>Line one Line two Line three</p>"
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_ordered_list_multiple_paragraphs_in_item():
    text = """1. This is the first paragraph of the first item.

   This is the second paragraph of the first item.
2. Second item"""
    expected = """<ol>
<li><p>This is the first paragraph of the first item.</p>
<p>This is the second paragraph of the first item.</p></li>
<li><p>Second item</p></li>
</ol>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_nested_unordered_list():
    text = """- Item one
  - Nested item one
  - Nested item two
- Item two"""
    expected = """<ul>
<li><p>Item one</p>
<ul>
<li><p>Nested item one</p></li>
<li><p>Nested item two</p></li>
</ul></li>
<li><p>Item two</p></li>
</ul>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_nested_ordered_list_in_unordered_list():
    text = """- Item one paragraph one

  Item one paragraph two

  1. Nested ordered item one
  2. Nested ordered item two
- Item two"""
    expected = """<ul>
<li><p>Item one paragraph one</p>
<p>Item one paragraph two</p>
<ol>
<li><p>Nested ordered item one</p></li>
<li><p>Nested ordered item two</p></li>
</ol></li>
<li><p>Item two</p></li>
</ul>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )


def test_outside_paragraph_and_list():
    text = """Outside paragraph line one
Outside paragraph line two

- List item one
- List item two

Outside paragraph again"""
    expected = """<p>Outside paragraph line one Outside paragraph line two</p>
<ul>
<li><p>List item one</p></li>
<li><p>List item two</p></li>
</ul>
<p>Outside paragraph again</p>"""
    assert equals_ignore_whitespace(
        _process_paragraphs_and_lists(text),
        expected
    )
