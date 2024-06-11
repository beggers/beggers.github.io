from __future__ import annotations
import re
from typing import Optional

from beneggerscom.ssg.input_files import InputFile

import logging

CSS_IMPORT_REGEX = re.compile(r"@import '(?P<file>.+?)';")


class StyleFile(InputFile):
    name: str
    content: str
    rendered_content: Optional[str] = None

    @classmethod
    def from_lines(cls, name: str, lines: list[str]):
        style_file = StyleFile()
        style_file.name = name
        style_file.content = "\n".join(lines)
        return style_file

    def render(self, styles: dict[str, StyleFile]) -> str:
        logging.debug("Rendering style %s", self.name)
        rendered = self.content
        match = CSS_IMPORT_REGEX.search(rendered)
        while match:
            logging.debug("Rendering import %s", match.group("file"))
            file = match.group("file")
            if file not in styles:
                raise ValueError(f"Style '{file}' not found.")
            rendered = rendered.replace(
                match.group(0), styles[file].render(styles)
            )
            match = CSS_IMPORT_REGEX.search(rendered)
        self.rendered_content = rendered
        return rendered
