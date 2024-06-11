def filename_to_url(path: str, protocol: str, hostname: str) -> str:
    if not protocol or not hostname:
        raise ValueError("Must specify protocol and hostname")
    parts: list[str] = path.split(".")
    if len(parts) > 2:
        raise ValueError(f"Multiple periods in path? {path}")
    path_without_extension: str = parts[0]
    fragments: list[str] = path_without_extension.split("/")
    if fragments[-1] == "index":
        fragments = fragments[:-1]
    fragments.reverse()
    url: str = ".".join([*fragments, hostname])
    if len(url) > 255:
        raise ValueError(f"URL too long. {url}")
    return protocol + "://" + url
