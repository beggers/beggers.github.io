def filename_to_url(path: str, protocol: str, hostname: str) -> str:
    if not protocol or not hostname:
        raise ValueError("Must specify protocol and hostname")
    parts = path.split(".")
    if len(parts) > 2:
        raise ValueError(f"Multiple periods in path? {path}")
    path = parts[0]
    url = path.split("/")
    if url[-1] == "index":
        url = url[:-1]
    url.reverse()
    url = ".".join([*url, hostname])
    if len(url) > 255:
        raise ValueError(f"URL too long. {url}")
    return protocol + "://" + url
