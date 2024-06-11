import re
from typing import Optional

from beneggerscom.ssg import SiteWideEvalContext
from beneggerscom.ssg.input_files.markdown import MarkdownFile
from beneggerscom.ssg.input_files.layout import LayoutFile

import logging

LAYOUT_INCLUDE_REGEX = re.compile(r"{% include (?P<layout>.+?) %}")


class Page:
    rendered_content: Optional[str]

    md: MarkdownFile
    layout: LayoutFile
    style: str
    site_wide_eval_context: SiteWideEvalContext
    partials: dict[str, LayoutFile]

    def __init__(self,
                 md: MarkdownFile,
                 layout: LayoutFile,
                 style: str,
                 site_wide_eval_context: SiteWideEvalContext,
                 partials: dict[str, LayoutFile],
                 ):
        self.md = md
        self.layout = layout
        self.rendered_content = None
        self.style = style

        self.site_wide_eval_context = site_wide_eval_context
        self.partials = partials

    def render(self) -> None:
        pass

    def _render_partials(self) -> None:
        rendered = self.layout.content
        include = LAYOUT_INCLUDE_REGEX.search(rendered)
        while include:
            logging.debug("Rendering include %s", include.group("layout"))
            partial_name = include.group("layout")
            if partial_name not in self.partials:
                raise ValueError(f"Partial '{partial_name}' not found.")
            # TODO Recursion limit
            # TODO This unnecessarily renders partials multiple times.
            rendered = rendered.replace(
                include.group(0),
                self.partials[partial_name].content
            )
            include = LAYOUT_INCLUDE_REGEX.search(rendered)
        self.rendered_content = rendered

    def write_to_file(self, path: str) -> None:
        pass
