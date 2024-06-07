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
def md_dir_single_file(tmp_path, valid_md_file):
    test_dir = tmp_path / "test"
    test_dir.mkdir()
    test_md = test_dir / "test.md"
    test_md.write_text(valid_md_file)
    return test_dir


def test_ingest_single_markdown_file(site_generator, md_dir_single_file):
    site_generator.ingest_markdown_directory(md_dir_single_file)
    assert len(site_generator.markdowns) == 1
    for k, v in site_generator.markdowns.items():
        assert k.endswith("test.md")
        assert v.title == "Test"
