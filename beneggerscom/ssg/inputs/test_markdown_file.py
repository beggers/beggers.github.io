import pytest

from beneggerscom.ssg.inputs.markdown_file import MarkdownFile


def test_markdown_file_title_and_meta_title():
    in_md = """
---
title: Test title
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile()
    md.from_markdown(in_md)
    assert md.title == "Test Title"
    assert md.meta_title == "Test Title | Ben Eggers dot com"


def test_markdown_file_raises_with_no_title():
    with pytest.raises(ValueError):
        in_md = """
---
---
""".strip().split(
            "\n"
        )
        md = MarkdownFile()
        md.from_markdown(in_md)


def test_markdown_file_description():
    in_md = """
---
title: Test title
description: test description
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile()
    md.from_markdown(in_md)
    assert md.description == "test description"


def test_markdown_file_manual_meta_title():
    in_md = """
---
title: Test title
meta_title: Test meta title
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile()
    md.from_markdown(in_md)
    assert md.title == "Test Title"
    assert md.meta_title == "Test meta title"


def test_markdown_file_date():
    in_md = """
---
title: Test title
date: 2024-06-07
---
""".strip().split(
        "\n"
    )
    md = MarkdownFile()
    md.from_markdown(in_md)
    assert md.date == "2024-06-07"


def test_markdown_file_raises_with_unknown_metadata():
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
        md = MarkdownFile()
        md.from_markdown(in_md)


def test_markdown_file_content():
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
    md = MarkdownFile()
    md.from_markdown(in_md_meta + in_md_content)
    assert md.date == "2024-06-07"
    assert md.content == "\n".join(in_md_content)
