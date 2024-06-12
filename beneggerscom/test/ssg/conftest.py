import pytest

from beneggerscom.ssg.input_files.markdown import MarkdownFile
from beneggerscom.ssg.page import EvalContext
from beneggerscom.ssg.site_generator import SiteGenerator


@pytest.fixture
def site_generator():
    return SiteGenerator(
        "example.com",
        "Test Site",
        "A test site",
        "https",
        "default",
        "default",
    )


@pytest.fixture
def valid_md_file_text():
    return """---
title: Test
---
Here's a paragraph
"""


@pytest.fixture
def valid_style_file_text():
    return """body {
    background-color: red;
}
"""


@pytest.fixture
def valid_layout_file_text():
    return """<!DOCTYPE html>"""


@pytest.fixture
def valid_partial_file_text():
    return """
{% define partial1 %}
<footer>
{% end partial1 %}
"""


@pytest.fixture
def base_eval_context():
    e = EvalContext()
    e.base_url = "example.com"
    e.protocol = "https"
    e.pages = []
    e.posts = []
    e.page = None
    e.slot = ""
    return e


@pytest.fixture
def valid_md_file(valid_md_file_text):
    return MarkdownFile.from_lines(valid_md_file_text.split("\n"))


@pytest.fixture
def md_dir_illegal_ext(tmp_path, valid_md_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.txt"
    test_md.write_text(valid_md_file_text)
    return test_dir.as_posix()


@pytest.fixture
def md_dir_single_file(tmp_path, valid_md_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.md"
    test_md.write_text(valid_md_file_text)
    return test_dir.as_posix()


@pytest.fixture
def md_dir_with_subdir(tmp_path, valid_md_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.md"
    test_md.write_text(valid_md_file_text)

    test_dir2 = test_dir / "test_again"
    test_dir2.mkdir()
    test_md2 = test_dir2 / "test_again.md"
    test_md2.write_text(valid_md_file_text)

    return test_dir.as_posix()


@pytest.fixture
def styles_dir_illegal_ext(tmp_path, valid_style_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_style = test_dir / "test.txt"
    test_style.write_text(valid_style_file_text)
    return test_dir.as_posix()


@pytest.fixture
def styles_dir_single_file(tmp_path, valid_style_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_style = test_dir / "test.css"
    test_style.write_text(valid_style_file_text)
    return test_dir.as_posix()


@pytest.fixture
def styles_dir_with_subdir(tmp_path, valid_style_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_style = test_dir / "test.css"
    test_style.write_text(valid_style_file_text)

    test_dir2 = test_dir / "test_again"
    test_dir2.mkdir()
    test_style2 = test_dir2 / "test_again.css"
    test_style2.write_text(valid_style_file_text)

    return test_dir.as_posix()


@pytest.fixture
def layouts_dir_illegal_ext(tmp_path, valid_layout_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_layout = test_dir / "test.txt"
    test_layout.write_text(valid_layout_file_text)
    return test_dir.as_posix()


@pytest.fixture
def layouts_dir_single_file(tmp_path, valid_layout_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_layout = test_dir / "test.html"
    test_layout.write_text(valid_layout_file_text)
    return test_dir.as_posix()


@pytest.fixture
def partials_dir_single_file(tmp_path, valid_partial_file_text):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_partial = test_dir / "different_from_partial_name.html"
    test_partial.write_text(valid_partial_file_text)
    return test_dir.as_posix()


@pytest.fixture
def layouts_dir_with_layout_and_partial(
    tmp_path,
    valid_layout_file_text,
    valid_partial_file_text
):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_layout = test_dir / "test.html"
    test_layout.write_text(valid_layout_file_text)

    test_partial = test_dir / "different_from_partial_name.html"
    test_partial.write_text(valid_partial_file_text)

    return test_dir.as_posix()
