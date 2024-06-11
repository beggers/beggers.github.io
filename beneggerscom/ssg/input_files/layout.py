from __future__ import annotations
import re

from beneggerscom.ssg.input_files import InputFile

import logging

LAYOUT_INCLUDE_REGEX = re.compile(r"{% include (?P<layout>.+?) %}")
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

    def _render_partials(self, partials: dict[str, LayoutFile]) -> str:
        rendered = self.content
        include = LAYOUT_INCLUDE_REGEX.search(rendered)
        while include:
            logging.debug("Rendering include %s", include.group("layout"))
            partial_name = include.group("layout")
            if partial_name not in partials:
                raise ValueError(f"Partial '{partial_name}' not found.")
            # TODO Recursion limit
            # TODO This unnecessarily renders partials multiple times.
            rendered = rendered.replace(
                include.group(0),
                partials[partial_name]._render_partials(partials)
            )
            include = LAYOUT_INCLUDE_REGEX.search(rendered)
        rendered_content = self.content
        for partial_name, partial in partials.items():
            rendered_content = rendered_content.replace(
                f"{{% include {partial_name} %}}", partial.content
            )
        return rendered_content
