import pytest

from beneggerscom.ssg.input_files.layout import LayoutFile


def test_full_layout():
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    assert not layout_file.partial
    assert not layout_file.name
    assert layout_file.content == "<!DOCTYPE html>"


def test_full_layout_with_name():
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("name", layout)
    assert layout_file.name == "name"
    assert layout_file.content == "<!DOCTYPE html>"


def test_partial_layout_raises_if_no_end():
    layout = """
{% define test %}
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    with pytest.raises(ValueError):
        LayoutFile.from_lines("", layout)


def test_partial_layout_raises_if_no_match():
    layout = """
{% define test %}
<!DOCTYPE html>
{% end not_test %}
""".strip().split(
        "\n"
    )
    with pytest.raises(ValueError):
        LayoutFile.from_lines("", layout)


def test_partial_layout():
    layout = """
{% define test %}
<!DOCTYPE html>
{% end test %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    assert layout_file.partial
    assert layout_file.name == "test"
    assert layout_file.content == "<!DOCTYPE html>"


def test_render_partials_no_partials():
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_lines("", layout)
    assert layout_file._render_partials({}) == "<!DOCTYPE html>"


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
    assert layout_file._render_partials(
        {"partial": partial_file}
    ) == "<!DOCTYPE html>\n<html>"


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
    assert layout_file._render_partials(
        {"partial": partial_file, "partial2": partial2_file}
    ) == "<!DOCTYPE html>\n<html>\n<body>"


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
    assert layout_file._render_partials(
        {"partial": partial_file, "partial2": partial2_file}
    ) == "<!DOCTYPE html>\n<html>\n<body>"
