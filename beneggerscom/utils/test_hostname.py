import pytest

from beneggerscom.utils.hostname import filename_to_url


def test_raises_if_too_many_periods_in_path():
    with pytest.raises(ValueError):
        filename_to_url("test.filename.md", "http", "localhost")


def test_raises_if_no_protocol():
    with pytest.raises(ValueError):
        filename_to_url("filename", "", "localhost")


def test_raises_if_no_hostname():
    with pytest.raises(ValueError):
        filename_to_url("filename", "http", "")


def test_url_honors_protocol():
    url = filename_to_url("filename", "http", "localhost")
    assert url.startswith("http://")

    url = filename_to_url("filename", "https", "localhost")
    assert url.startswith("https://")

    url = filename_to_url("filename", "ssh", "localhost")
    assert url.startswith("ssh://")


def test_url_honors_hostname():
    url = filename_to_url("filename", "http", "localhost")
    assert url.endswith("localhost")

    url = filename_to_url("filename", "http", "beneggers.com")
    assert url.endswith("beneggers.com")

    url = filename_to_url("filename", "http", "something.outlandish.gov")
    assert url.endswith("something.outlandish.gov")


def test_url_starts_with_filename():
    url = filename_to_url("filename", "http", "localhost")
    assert url.startswith("http://filename")


def test_url_gets_rid_of_file_extension():
    url = filename_to_url("filename.txt", "http", "localhost")
    assert url == "http://filename.localhost"


def test_url_contains_subdirectories():
    url = filename_to_url(
        "dir/subdir/subsubdir/filename.md", "http", "localhost"
    )
    assert url == "http://filename.subsubdir.subdir.dir.localhost"


def test_url_shaves_off_index():
    url = filename_to_url("directory/index.md", "http", "localhost")
    assert url == "http://directory.localhost"


def test_url_shaves_off_index_at_root():
    url = filename_to_url("index.md", "http", "localhost")
    assert url == "http://localhost"
