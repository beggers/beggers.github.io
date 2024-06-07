import pytest

from beneggerscom.ssg.input_files.markdown import MarkdownFile


def test_title_and_meta_title():
    in_md = """
---
title: Test title
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.title == "Test Title"
    assert md.meta_title == "Test Title | Ben Eggers dot com"


def test_raises_with_no_title():
    with pytest.raises(ValueError):
        in_md = """
---
---
""".strip().split(
            "\n"
        )
        MarkdownFile.from_markdown(in_md)


def test_description():
    in_md = """
---
title: Test title
description: test description
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.description == "test description"


def test_manual_meta_title():
    in_md = """
---
title: Test title
meta_title: Test meta title
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.title == "Test Title"
    assert md.meta_title == "Test meta title"


def test_date():
    in_md = """
---
title: Test title
date: 2024-06-07
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.date == "2024-06-07"


def test_raises_with_unknown_metadata():
    with pytest.raises(ValueError):
        in_md = """
---
title: Test title
date: 2024-06-07
something_else: yeah
---
""".strip().split(
            "\n"
        )
        MarkdownFile.from_markdown(in_md)


def test_content():
    in_md_meta = """
---
title: Test title
date: 2024-06-07
---
""".strip().split(
        "\n"
    )
    in_md_content = """
Here's some content.

Here's some more.
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md_meta + in_md_content)
    assert md.date == "2024-06-07"
    assert md.content == "\n".join(in_md_content)


def test_layout():
    in_md = """
---
title: Test title
layout: about.html
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.layout == "about.html"


def test_nav_raises_if_not_int():
    with pytest.raises(ValueError):
        in_md = """
---
title: Test title
nav: not an int
---
""".strip().split(
            "\n"
        )
        MarkdownFile.from_markdown(in_md)


def test_nav_defaults_to_negative_one():
    in_md = """
---
title: Test title
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.nav == -1


def test_nav_parses():
    in_md = """
---
title: Test title
nav: 4
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.nav == 4


def test_content_as_html_basic_paragraph():
    in_md = """
---
title: Test title
layout: about.html
---
Here's some content
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert md.content_as_html() == "<p>Here's some content</p>"


def test_content_as_html_multiple_paragraphs():
    in_md = """
---
title: Test title
layout: about.html
---
Here's some content

Here's some more
""".strip().split(
        "\n"
    )
    md = MarkdownFile.from_markdown(in_md)
    assert (
        md.content_as_html()
        == """<p>Here's some content</p>
<p>Here's some more</p>"""
    )


# We're not going to test all the functionality of the markdown library.
