import re

FOOTNOTE_START_REGEX = r'<div class="footnote">'
FOOTNOTE_END_REGEX = r"</div>"
SECTION_END_REGEX = r"</section>"
SECTION_END_TEXT = "</section>\n"

FOOTNOTE_PARAGRAPH_REGEX = r"<p>\s*\[\^(?P<id>\d+)\]:(?P<text>.+?)\s*</p>"


def move_footnotes_to_own_section(html: str) -> str:
    # Find the beginning of the footnote div
    footnote_start = html.find(FOOTNOTE_START_REGEX)
    # Find the end of the footnote div
    footnote_end = html.find(FOOTNOTE_END_REGEX, footnote_start) + len(
        FOOTNOTE_END_REGEX
    )
    # Find the first </section> after the end of the footnote
    section_end = html.find(SECTION_END_REGEX, footnote_end)
    # Remove the </section> from there and put it before the footnote div
    html = (
        html[:footnote_start]
        + SECTION_END_TEXT
        + html[footnote_start:footnote_end]
        + html[section_end + len(SECTION_END_TEXT) :]
    )
    return html


def add_footnote_class_to_footnote_paragraphs(html: str) -> str:
    match = re.search(FOOTNOTE_PARAGRAPH_REGEX, html, re.DOTALL)
    while match:
        html = html.replace(
            match.group(),
            f'<p class="footnote">\n[^{match.group("id")}]:{match.group("text")}\n</p>',
        )
        match = re.search(FOOTNOTE_PARAGRAPH_REGEX, html, re.DOTALL)
    return html
