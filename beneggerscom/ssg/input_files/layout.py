from beneggerscom.ssg.input_files import InputFile

import re

import logging

LAYOUT_DEF_REGEX = re.compile(r"{% define (?P<layout>.+?) %}")
LAYOUT_END_REGEX = re.compile(r"{% end (?P<layout>.+?) %}")


class LayoutFile(InputFile):
    name: str
    content: str
    # TODO: Separate partial class? Separate partial directory?
    partial: bool

    def from_layout(self, lines: list[str]):
        start_match = LAYOUT_DEF_REGEX.match(lines[0])
        if start_match:
            logging.debug(
                "Layout is a named template => partial: %s",
                start_match.group("layout"),
            )
            self.name = start_match.group("layout")
            end_match = LAYOUT_END_REGEX.match(lines[-1])
            if not end_match:
                raise ValueError("Layout definition does not end correctly.")
            if end_match.group("layout") != self.name:
                raise ValueError("Layout name does not match end.")

            content = "\n".join(lines[1:-1])
            self.partial = True
            logging.debug("Partial content: %s", content)
        else:
            content = "\n".join(lines)
            self.partial = False
            logging.debug("Layout content: %s", content)
