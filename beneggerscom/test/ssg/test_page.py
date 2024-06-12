import pytest

from beneggerscom.ssg.input_files.layout import LayoutFile
from beneggerscom.ssg.page import Page


def test_render_partials_no_partials(valid_md_file):
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    page._render_partials({})
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_partials_one_partial(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
""".strip().split(
        "\n"
    )
    partial = """
{% define partial %}
<html>
{% end partial %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    partial_file = LayoutFile.from_lines("", partial)
    page = Page(valid_md_file, layout_file, "")
    page._render_partials({"partial": partial_file})
    assert page._rendered_content == "<!DOCTYPE html>\n<html>"


def test_render_partials_multiple_sibling_partials(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
{% include partial2 %}
""".strip().split(
        "\n"
    )
    partial = """
{% define partial %}
<html>
{% end partial %}
""".strip().split(
        "\n"
    )
    partial2 = """
{% define partial2 %}
<body>
{% end partial2 %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    partial_file = LayoutFile.from_lines("", partial)
    partial2_file = LayoutFile.from_lines("", partial2)
    page = Page(valid_md_file, layout_file, "")
    page._render_partials({"partial": partial_file, "partial2": partial2_file})
    assert page._rendered_content == "<!DOCTYPE html>\n<html>\n<body>"


def test_render_partials_nested_partials(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
""".strip().split(
        "\n"
    )
    partial = """
{% define partial %}
<html>
{% include partial2 %}
{% end partial %}
""".strip().split(
        "\n"
    )
    partial2 = """
{% define partial2 %}
<body>
{% end partial2 %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    partial_file = LayoutFile.from_lines("", partial)
    partial2_file = LayoutFile.from_lines("", partial2)
    page = Page(valid_md_file, layout_file, "")
    page._render_partials({"partial": partial_file, "partial2": partial2_file})
    assert page._rendered_content == "<!DOCTYPE html>\n<html>\n<body>"


def test_render_partials_missing_partial(valid_md_file):
    layout = """
<!DOCTYPE html>
{% include partial %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    with pytest.raises(ValueError) as e:
        page._render_partials({})
    assert str(e.value) == "Partial 'partial' not found."


def test_render_loops_no_loops(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    page._render_loops(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_loops_raises_if_no_end(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{{ page.title }}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    with pytest.raises(ValueError):
        page._render_loops(base_eval_context)


def test_render_loops_empty_loop(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{% page.title %}
{% end %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    page._render_loops(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>\n"


def test_render_loops_single_loop(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for page in pages %}
{% page.title %}
{% end %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    base_eval_context.pages = [page, page, page]
    page._render_loops(base_eval_context)
    assert (
        "".join(page._rendered_content.split('\n'))
        == "".join("<!DOCTYPE html>TestTestTest")
    )


def test_render_loop_with_if_statement(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% for i in sorted([p for p in pages if p.nav != -1], key=lambda p: p.nav) %}
{% i.nav %}
{% end %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page1 = Page(valid_md_file, layout_file, "")
    page2 = Page(valid_md_file, layout_file, "")
    page3 = Page(valid_md_file, layout_file, "")
    page1.nav = 1
    page2.nav = 2
    page3.nav = 3
    pages = [page1, page2, page3]
    base_eval_context.pages = pages
    page1._render_loops(base_eval_context)
    assert (
        "".join(page1._rendered_content.split('\n'))
        == "".join("<!DOCTYPE html>123")
    )


def test_render_variables_no_variables(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    page._render_variables(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>"


def test_render_variables_single_variable(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% page.title %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(valid_md_file, layout_file, "")
    base_eval_context.page = page
    page._render_variables(base_eval_context)
    assert page._rendered_content == "<!DOCTYPE html>\nTest"


def test_render_variables_multiple_variables(valid_md_file, base_eval_context):
    layout = """
<!DOCTYPE html>
{% page.title %}
{% page.date %}
{% base_url %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    valid_md_file.date = "2021-01-01"

    page = Page(valid_md_file, layout_file, "")
    base_eval_context.base_url = "localhost"
    base_eval_context.page = page

    page._render_variables(base_eval_context)
    assert (
        "".join(page._rendered_content.split('\n'))
        == "".join("<!DOCTYPE html>Test2021-01-01localhost")
    )
