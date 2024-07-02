import re


BOLD_REGEX = r"\*\*(.*?)\*\*|__([^_]*?)__"
HEADER_REGEX = r"^(#+)\s(.+)"
ITALICS_REGEX = r"\*(.*?)\*|_([^_]*?)_"
LINK_REGEX = r"\[([^\]]+)\]\(([^)]+)\)"


def to_html(raw_md: str) -> str:
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


def _process_lists(raw_md: str) -> str:
    return raw_md


def _process_sidenotes(raw_md: str) -> str:
    return raw_md


def _process_paragraphs(raw_md: str) -> str:
    return raw_md


# Headers
# Paragraphs (implies paragraph detection)
# Lists
# Nested lists
# Links
# Bold and italic
# Footnotes
#
# We can do this line-by-line or regex-by-regex
#
# Line-by-line pros:
# - Easier paragraph detection (do I really want or need paragraph detection?)
# - Context on lists and list indentation.
# Line-by-line cons:
# - Lots of state to track exactly where we are.
#   - Really only for lists and nested lists.
#
# Regex-by-regex pros:
# - Headers become eassssssy. If we skip paragraph detection
# - Bold, italic, and links become easy af.
#
# Plan:
# - Bold: regex in loop
# - Italic: regex in loop
# - Headers: regex in loop. Add a newline at the end to make paragraphs check
#            out lmao
# - Links: Regex in loop.
# -
