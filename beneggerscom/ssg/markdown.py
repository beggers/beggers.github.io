# I couldn't find a markdown processor that handles sidenotes how I want.
# So here we are.

import re
from typing import Tuple


BOLD_REGEX = r"\*\*(.*?)\*\*|__([^_]*?)__"
HEADER_REGEX = r"^(#+)\s(.+)"
ITALICS_REGEX = r"\*(.*?)\*|_([^_]*?)_"
LINK_REGEX = r"\[([^\]]+)\]\(([^)]+)\)"


def str_to_html(raw_md: str) -> str:
    html = _process_headings(raw_md)
    html = _process_paragraphs_and_lists(html)
    html = _process_links(html)
    html = _process_bolds(html)
    html = _process_italics(html)
    return html


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
    in_paragraph = False
    # Each element is (indent_level, "ul" or "ol")
    list_stack: list[Tuple[int, str]] = []
    in_list_item = False

    def close_paragraph():
        nonlocal in_paragraph
        if in_paragraph:
            output_lines.append("</p>")
            in_paragraph = False

    def close_list_item():
        nonlocal in_list_item
        if in_list_item:
            close_paragraph()
            output_lines.append("</li>")
            in_list_item = False

    def close_all_lists():
        nonlocal list_stack, in_list_item
        close_list_item()
        while list_stack:
            _, ltype = list_stack.pop()
            output_lines.append(f"</{ltype}>")

    def start_paragraph():
        nonlocal in_paragraph
        if not in_paragraph:
            output_lines.append("<p>")
            in_paragraph = True

    def start_list_item():
        nonlocal in_list_item
        close_list_item()
        output_lines.append("<li>")
        in_list_item = True

    def close_lists_down_to(indent_level):
        nonlocal list_stack
        while list_stack and list_stack[-1][0] > indent_level:
            close_list_item()
            _, ltype = list_stack.pop()
            output_lines.append(f"</{ltype}>")

    def detect_list_item(line):
        spaces = 0
        for ch in line:
            if ch == ' ':
                spaces += 1
            else:
                break
        content_after_spaces = line[spaces:]

        if re.match(r"^[-\*\+]\s", content_after_spaces):
            return spaces, "ul", content_after_spaces[2:]
        elif re.match(r"^\d+\.\s", content_after_spaces):
            m = re.match(r"^\d+\.\s+(.*)", content_after_spaces)
            if m:
                return spaces, "ol", m.group(1)
        return None

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("<h"):
            close_paragraph()
            close_all_lists()
            output_lines.append(line)
            continue

        if not stripped:
            if in_list_item:
                close_paragraph()
            else:
                close_paragraph()
            continue

        list_item_info = detect_list_item(line)
        if list_item_info is not None:
            current_indent, list_type, list_content = list_item_info

            if not list_stack:
                close_paragraph()
                output_lines.append(f"<{list_type}>")
                list_stack.append((current_indent, list_type))
                start_list_item()
            else:
                if current_indent > list_stack[-1][0]:
                    close_paragraph()
                    output_lines.append(f"<{list_type}>")
                    list_stack.append((current_indent, list_type))
                    start_list_item()
                else:
                    close_lists_down_to(current_indent)
                    if list_stack and list_stack[-1][1] != list_type:
                        close_list_item()
                        _, old_type = list_stack.pop()
                        output_lines.append(f"</{old_type}>")
                        output_lines.append(f"<{list_type}>")
                        list_stack.append((current_indent, list_type))
                        start_list_item()
                    else:
                        start_list_item()

            if list_content.strip():
                start_paragraph()
                output_lines.append(list_content.strip())
        else:
            if list_stack:
                if not in_list_item:
                    close_all_lists()
                    start_paragraph()
                    output_lines.append(stripped)
                else:
                    if not in_paragraph:
                        start_paragraph()
                    else:
                        output_lines.append(" ")
                    output_lines.append(stripped)
            else:
                if not in_paragraph:
                    start_paragraph()
                else:
                    output_lines.append(" ")
                output_lines.append(stripped)

    close_paragraph()
    close_all_lists()

    return "\n".join(output_lines)
