from beneggerscom.ssg.input_files import InputFile

import re
from typing import Optional

import logging

LAYOUT_DEF_REGEX = re.compile(r"{% define (?P<layout>.+?) %}")
LAYOUT_END_REGEX = re.compile(r"{% end (?P<layout>.+?) %}")


class LayoutFile(InputFile):
    content: str
    name: str
    # TODO: Separate partial class? Separate partial directory?
    partial: bool = False

    @classmethod
    def from_lines(_cls, default_name: str, lines: list[str]):
        layout_file = LayoutFile()
        layout_file.name = default_name
        start_match = LAYOUT_DEF_REGEX.match(lines[0])
        if start_match:
            logging.debug(
                "Layout is a named template => partial: %s",
                start_match.group("layout"),
            )
            layout_file.name = start_match.group("layout")
            end_match = LAYOUT_END_REGEX.match(lines[-1])
            if not end_match:
                raise ValueError("Layout definition does not end correctly.")
            if end_match.group("layout") != layout_file.name:
                raise ValueError("Layout name does not match end.")

            layout_file.content = "\n".join(lines[1:-1])
            layout_file.partial = True
            logging.debug("Partial content: %s", layout_file.content)
        else:
            layout_file.content = "\n".join(lines)
            layout_file.partial = False
            logging.debug("Layout content: %s", layout_file.content)
        return layout_file
