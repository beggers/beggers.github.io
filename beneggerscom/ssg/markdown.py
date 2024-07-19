import re


BOLD_REGEX = r"\*\*(.*?)\*\*|__([^_]*?)__"
HEADER_REGEX = r"^(#+)\s(.+)"
ITALICS_REGEX = r"\*(.*?)\*|_([^_]*?)_"
LINK_REGEX = r"\[([^\]]+)\]\(([^)]+)\)"


def str_to_html(raw_md: str) -> str:
    return raw_md


def _process_headings(raw_md: str) -> str:
    def replace_with_header(match):
        header_level = len(match.group(1))
        header_text = match.group(2).strip()
        return f"<h{header_level}>{header_text}</h{header_level}>"
    return re.sub(
        HEADER_REGEX,
        replace_with_header,
        raw_md,
        flags=re.MULTILINE
    )


def _process_bolds(raw_md: str) -> str:
    def replace_with_strong(match):
        return f"<strong>{match.group(1) or match.group(2)}</strong>"
    return re.sub(BOLD_REGEX, replace_with_strong, raw_md)


def _process_italics(raw_md: str) -> str:
    def replace_with_em(match):
        return f"<em>{match.group(1) or match.group(2)}</em>"
    return re.sub(ITALICS_REGEX, replace_with_em, raw_md)


def _process_links(raw_md: str) -> str:
    def replace_with_a(match):
        return f'<a href="{match.group(2)}">{match.group(1)}</a>'
    return re.sub(LINK_REGEX, replace_with_a, raw_md)


def _process_paragraphs_and_lists(raw_md: str) -> str:
    lines = raw_md.split("\n")
    output_lines = []

    # Whether we're starting a new paragraph, i.e. whether the previous line
    # was empty.
    fresh_paragraph = True
    # Number of spaces at the start of each line of the current list.
    # For nested lists, we store the total indentation -- NOT the indentation
    # relative to the parent list.
    # NB: This also encodes how many layers of list we're in.
    list_indentations = []
    # A single HTML paragraph can span multiple lines of markdown.
    current_paragraph = ""

    for line in lines:
        if not line or line.startswith("#"):
            output_lines.append(current_paragraph)
            current_paragraph = ""
            fresh_paragraph = True
            continue
        

    return raw_md
