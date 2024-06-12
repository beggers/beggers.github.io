import pytest


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


def test_ingest_single_style_file(site_generator, styles_dir_single_file):
    site_generator.ingest_styles_directory(styles_dir_single_file)
    assert len(site_generator.styles) == 1
    for k, v in site_generator.styles.items():
        assert k.endswith("test.css")
        assert v.name == "test.css"


def test_ingest_styles_files_subdir(site_generator, styles_dir_with_subdir):
    site_generator.ingest_styles_directory(styles_dir_with_subdir)
    assert len(site_generator.styles) == 2
    assert any(
        map(
            lambda s: "test_again/test_again.css" in s,
            site_generator.styles.keys(),
        )
    )


def test_ingest_styles_raises_on_double_ingest(
    site_generator, styles_dir_single_file
):
    site_generator.ingest_styles_directory(styles_dir_single_file)
    with pytest.raises(ValueError):
        site_generator.ingest_styles_directory(styles_dir_single_file)


def test_ingest_styles_raises_if_non_css_extension_found(
    site_generator, styles_dir_illegal_ext
):
    with pytest.raises(ValueError):
        site_generator.ingest_styles_directory(styles_dir_illegal_ext)


def test_ingest_single_layout_file(site_generator, layouts_dir_single_file):
    site_generator.ingest_layouts_directory(layouts_dir_single_file)
    assert len(site_generator.layouts) == 1
    for k, v in site_generator.layouts.items():
        assert k == "test.html"
        assert v.name == "test.html"


def test_ingest_single_partial_file(site_generator, partials_dir_single_file):
    site_generator.ingest_layouts_directory(partials_dir_single_file)
    assert len(site_generator.partials) == 1
    for k, v in site_generator.partials.items():
        assert k == "partial1"
        assert v.name == "partial1"
        assert v.partial


def test_ingest_layout_and_partial(
    site_generator,
    layouts_dir_with_layout_and_partial
):
    site_generator.ingest_layouts_directory(
        layouts_dir_with_layout_and_partial
    )
    assert len(site_generator.layouts) == 1
    assert len(site_generator.partials) == 1
    for k, v in site_generator.layouts.items():
        assert k == "test.html"
        assert v.name == "test.html"
    for k, v in site_generator.partials.items():
        assert k == "partial1"
        assert v.name == "partial1"
        assert v.partial


def test_ingest_layouts_raises_on_double_ingest(
    site_generator, layouts_dir_single_file
):
    site_generator.ingest_layouts_directory(layouts_dir_single_file)
    with pytest.raises(ValueError):
        site_generator.ingest_layouts_directory(layouts_dir_single_file)


def test_ingest_layouts_raises_if_non_html_extension_found(
    site_generator, layouts_dir_illegal_ext
):
    with pytest.raises(ValueError):
        site_generator.ingest_layouts_directory(layouts_dir_illegal_ext)
