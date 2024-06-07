import pytest

from beneggerscom.ssg.input_files.layout import LayoutFile


def test_full_layout():
    layout = """
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_layout(layout)
    print(layout_file.__dict__)
    assert not layout_file.partial
    assert not layout_file.name
    assert layout_file.content == "<!DOCTYPE html>"


def test_partial_layout_raises_if_no_end():
    layout = """
{% define test %}
<!DOCTYPE html>
""".strip().split(
        "\n"
    )
    with pytest.raises(ValueError):
        LayoutFile.from_layout(layout)


def test_partial_layout_raises_if_no_match():
    layout = """
{% define test %}
<!DOCTYPE html>
{% end not_test %}
""".strip().split(
        "\n"
    )
    with pytest.raises(ValueError):
        LayoutFile.from_layout(layout)


def test_partial_layout():
    layout = """
{% define test %}
<!DOCTYPE html>
{% end test %}
""".strip().split(
        "\n"
    )
    layout_file = LayoutFile.from_layout(layout)
    print(layout_file.__dict__)
    assert layout_file.partial
    assert layout_file.name == "test"
    assert layout_file.content == "<!DOCTYPE html>"
