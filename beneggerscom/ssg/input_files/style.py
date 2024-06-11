from __future__ import annotations
import re

from beneggerscom.ssg.input_files import InputFile

import logging

CSS_IMPORT_REGEX = re.compile(r"@import '(?P<file>.+?)';")


class StyleFile(InputFile):
    name: str
    content: str

    @classmethod
    def from_lines(cls, name: str, lines: list[str]):
        style_file = StyleFile()
        style_file.name = name
        style_file.content = "\n".join(lines)
        return style_file

    def materialize(self, styles: dict[str, StyleFile]) -> str:
        logging.debug("Materializing style %s", self.name)
        materialized = self.content
        match = CSS_IMPORT_REGEX.search(materialized)
        while match:
            logging.debug("materializing import %s", match.group("file"))
            file = match.group("file")
            if file not in styles:
                raise ValueError(f"Style '{file}' not found.")
            materialized = materialized.replace(
                # TODO recursion limit.
                # TODO this unnecessarily materializs imports multiple times.
                match.group(0), styles[file].materialize(styles)
            )
            match = CSS_IMPORT_REGEX.search(materialized)
        return materialized
