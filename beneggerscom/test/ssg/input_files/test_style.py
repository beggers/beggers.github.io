from beneggerscom.ssg.input_files.style import StyleFile

# TODO rewrite these to use fixtures


def test_style_file():
    style = """
body {
    font-family: Arial, sans-serif;
}
""".strip().split(
        "\n"
    )
    style_file = StyleFile.from_lines("style.css", style)
    assert style_file.name == "style.css"
    assert "".join(style_file.content.split()) == "".join(
        "body{\nfont-family: Arial, sans-serif;\n}".split()
    )


def test_style_file_materialize_with_no_imports():
    style = """
body {
    font-family: Arial, sans-serif;
}
""".strip().split(
        "\n"
    )
    style_file = StyleFile.from_lines("style.css", style)
    assert style_file.materialize({}) == style_file.content


def test_style_file_materialize_with_one_level_of_imports():
    style = """
@import 'other.css';
body {
    font-family: Arial, sans-serif;
}
""".strip().split(
        "\n"
    )
    other_style = """
h1 {
    color: red;
}
""".strip().split(
        "\n"
    )
    style_file = StyleFile.from_lines("style.css", style)
    other_style_file = StyleFile.from_lines("other.css", other_style)
    materialized = style_file.materialize({"other.css": other_style_file})
    assert "".join(materialized.split()) == "".join("""
h1 {
    color: red;
}
body {
    font-family: Arial, sans-serif;
}
""".split()
    )


def test_style_file_materialize_with_two_levels_of_imports():
    style = """
@import 'other.css';
body {
    font-family: Arial, sans-serif;
}
""".strip().split(
        "\n"
    )
    other_style = """
@import 'another.css';
h1 {
    color: red;
}
""".strip().split(
        "\n"
    )
    another_style = """
h2 {
    font-weight: bold;
}
""".strip().split(
        "\n"
    )
    style_file = StyleFile.from_lines("style.css", style)
    other_style_file = StyleFile.from_lines("other.css", other_style)
    another_style_file = StyleFile.from_lines("another.css", another_style)
    materialized = style_file.materialize(
        {"other.css": other_style_file, "another.css": another_style_file}
    )
    assert "".join(materialized.split()) == "".join("""
h2 {
    font-weight: bold;
}
h1 {
    color: red;
}
body {
    font-family: Arial, sans-serif;
}
""".split()
    )
