from beneggerscom.ssg.input_files.style import StyleFile


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
    assert "".join(style_file.content.split(" ")) == "".join(
        "body{\nfont-family: Arial, sans-serif;\n}".split(" ")
    )
