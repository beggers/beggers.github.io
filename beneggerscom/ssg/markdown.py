import re


HEADER_REGEX = r"^(#+)\s(.+)"


def to_html(raw_md: str) -> str:
    return raw_md


def _process_headings(raw_md: str) -> str:
    processed = raw_md
    for match in re.finditer(HEADER_REGEX, processed, re.MULTILINE):
        header_level = len(match.group(1))
        header_text = match.group(2)
        header_tag = f"<h{header_level}>{header_text}</h{header_level}>"
        # Replace the whole match with the corresponding header tag
        processed = processed.replace(match.group(0), header_tag)
    return processed


def _process_bolds(raw_md: str) -> str:
    return raw_md


def _process_italics(raw_md: str) -> str:
    return raw_md


def _process_links(raw_md: str) -> str:
    return raw_md


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
