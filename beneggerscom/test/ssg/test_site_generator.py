import pytest

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
def valid_md_file():
    return """---
title: Test
---
Here's a paragraph

And another
"""


@pytest.fixture
def md_dir_illegal_ext(tmp_path, valid_md_file):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.txt"
    test_md.write_text(valid_md_file)
    return test_dir


@pytest.fixture
def md_dir_single_file(tmp_path, valid_md_file):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.md"
    test_md.write_text(valid_md_file)
    return test_dir


@pytest.fixture
def md_dir_with_subdir(tmp_path, valid_md_file):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.md"
    test_md.write_text(valid_md_file)

    test_dir2 = test_dir / "test_again"
    test_dir2.mkdir()
    test_md2 = test_dir2 / "test_again.md"
    test_md2.write_text(valid_md_file)

    return test_dir


def test_ingest_single_markdown_file(site_generator, md_dir_single_file):
    site_generator.ingest_markdown_directory(md_dir_single_file)
    assert len(site_generator.markdowns) == 1
    for k, v in site_generator.markdowns.items():
        assert k.endswith("test.md")
        assert v.title == "Test"


def test_ingest_markdown_files_subdir(site_generator, md_dir_with_subdir):
    site_generator.ingest_markdown_directory(md_dir_with_subdir)
    assert len(site_generator.markdowns) == 2
    assert any(
        map(
            lambda s: "test/test_again/test_again.md" in s,
            site_generator.markdowns.keys(),
        )
    )


def test_ingest_markdown_raises_on_double_ingest(
    site_generator, md_dir_single_file
):
    site_generator.ingest_markdown_directory(md_dir_single_file)
    with pytest.raises(ValueError):
        site_generator.ingest_markdown_directory(md_dir_single_file)


def test_ingest_markdown_raises_if_non_md_extension_found(
    site_generator, md_dir_illegal_ext
):
    with pytest.raises(ValueError):
        site_generator.ingest_markdown_directory(md_dir_illegal_ext)
