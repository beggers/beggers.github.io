from beneggerscom.ssg.input_files.layout import LayoutFile
from beneggerscom.ssg.page import Page


def test_render_partials_no_partials():
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    page = Page(None, layout_file, "", None, {})
    page._render_partials()
    assert page.rendered_content == "<!DOCTYPE html>"


def test_render_partials_one_partial():
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
    page = Page(None, layout_file, "", None, {"partial": partial_file})
    page._render_partials()
    assert page.rendered_content == "<!DOCTYPE html>\n<html>"


def test_render_partials_multiple_sibling_partials():
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
    page = Page(
        None,
        layout_file,
        "",
        None,
        {"partial": partial_file, "partial2": partial2_file}
    )
    page._render_partials()
    assert page.rendered_content == "<!DOCTYPE html>\n<html>\n<body>"


def test_render_partials_nested_partials():
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
    page = Page(
        None,
        layout_file,
        "",
        None,
        {"partial": partial_file, "partial2": partial2_file}
    )
    page._render_partials()
    assert page.rendered_content == "<!DOCTYPE html>\n<html>\n<body>"
