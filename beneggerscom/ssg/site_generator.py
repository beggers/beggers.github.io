import os
import re
import shutil
from typing import Optional

from beneggerscom.ssg.input_files.markdown import MarkdownFile
from beneggerscom.ssg.input_files.layout import LayoutFile
from beneggerscom.ssg.input_files.style import StyleFile

import logging


END_REGEX = re.compile(r"{% end %}")
FOR_REGEX = re.compile(r"{% for (?P<var>.+?) in (?P<iter>.+?) %}")
VARIABLE_REGEX = re.compile(r"{% (?P<var>.+?) %}")

DEFAULT_DESCRIPTION = "No description specified for this page, sorry!"


class SiteGenerator:
    def __init__(
        self,
        hostname: str,
        title: str,
        description: str,
        protocol: str,
        default_layout: str,
        default_style: str,
    ):
        self.site_config = {
            "url": hostname,
            "title": title,
            "description": description,
            "protocol": protocol,
            "default_layout": default_layout,
            "default_style": default_style,
        }
        logging.info("Site config: %s", self.site_config)

        self.static_dir: Optional[str] = None
        self.statics: list[str] = []

        self.markdown_dir: Optional[str] = None
        # Full path -> MarkdownFile
        self.markdowns: dict[str, MarkdownFile] = {}

        self.layouts_dir: Optional[str] = None
        # Layout name -> LayoutFile
        self.layouts: dict[str, LayoutFile] = {}
        self.partials: dict[str, LayoutFile] = {}

        self.styles_dir: Optional[str] = None
        # Style name -> StyleFile
        self.styles: dict[str, StyleFile] = {}
        # Style name -> rendered CSS suitable for direct inclusion into HTML
        self.rendered_styles: dict[str, str] = {}

    def ingest_markdown_directory(self, path: str) -> None:
        logging.info("Ingesting markdown directory %s", path)
        self.markdown_dir = path
        files = self._all_files_in_dir(path)
        for filename in files:
            if filename in self.markdowns:
                raise ValueError("Markdown file already ingested.")
            if not filename.endswith(".md"):
                raise ValueError(
                    "Markdown file {} does not end with .md.".format(filename)
                )
            logging.debug("Ingesting markdown file %s", filename)

            with open(filename, "r") as f:
                md = MarkdownFile.from_lines(f.readlines())
                self.markdowns[filename] = md

    def ingest_layouts_directory(self, path: str) -> None:
        logging.info("Ingesting layouts directory %s", path)
        self.layouts_dir = path
        files = self._all_files_in_dir(path)
        for filename in files:
            if filename in self.layouts:
                raise ValueError("Layout file already ingested.")
            logging.debug("Ingesting layout file %s", filename)

            with open(filename, "r") as f:
                default_layout_name = os.path.basename(filename)
                layout = LayoutFile.from_lines(
                    default_layout_name, f.readlines()
                )
                if layout.partial:
                    self.partials[layout.name] = layout
                else:
                    self.layouts[layout.name] = layout

    def ingest_static_directory(self, path: str) -> None:
        logging.info("Ingesting static directory %s", path)
        self.static_dir = path
        self.statics = self._all_files_in_dir(path)
        logging.debug("Static files: %s", self.statics)

    def ingest_styles_directory(self, path: str) -> None:
        self.styles_dir = path
        files = self._all_files_in_dir(path)
        for filename in files:
            if not path.endswith(".css"):
                raise ValueError(
                    "Style file {} does not end with .css.".format(path)
                )
            with open(filename, "r") as f:
                name = path.replace(self.styles_dir + "/", "")
                self.styles[name] = (
                    StyleFile.from_lines(name, f.readlines())
                )

    def _all_files_in_dir(self, path: str) -> list[str]:
        files = []
        for root, _, fs in os.walk(path):
            for f in fs:
                files.append(os.path.join(root, f))
        return files

    def render(self, path: str) -> None:
        logging.info("Rendering site to %s", path)
        if not self.static_dir:
            raise ValueError("No static directory set.")
        if not self.markdown_dir:
            raise ValueError("No markdown directory set.")
        if not self.layouts_dir:
            raise ValueError("No layouts directory set.")
        if not self.styles_dir:
            raise ValueError("No styles directory set.")

        self._render_styles()
        for md_path, md in self.markdowns.items():
            logging.debug("Rendering markdown file %s", md_path)
            self._render_page(md_path, md, path)
        self._copy_statics(path)

    def _render_styles(self) -> None:
        for style_name, style in self.styles.items():
            self.rendered_styles[style_name] = style.render(self.styles)

    def _copy_statics(self, path: str) -> None:
        if not self.static_dir:
            raise ValueError("No static directory set.")
        for static in self.statics:
            logging.debug("Copying static file %s", static)
            shutil.copy(static, static.replace(self.static_dir, path))

    def _render_page(self, md_path, md, path):
        layout_name = md.get("layout", self.site_config["default_layout"])
        logging.debug("Rendering page with layout %s", layout_name)
        if layout_name not in self.layouts:
            raise ValueError(f"Layout '{layout_name}' not found.")
        layout = self.layouts[layout_name]

        rendered = self._render_layout(layout, md)

        output_path = md_path.replace(self.markdown_dir, path).replace(
            ".md", ".html"
        )
        logging.info("Writing to %s", output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write(rendered)

    def _render_layout(self, layout, page):
        rendered = layout

        eval_variables = {
            "site": self.site_config,
            "page": page,
            "pages": list(self.markdowns.values()),
        }
        page["style"] = self.rendered_styles.get(
            page.get("style", ""),
            self.rendered_styles[self.site_config["default_style"]],
        )
        logging.debug("Eval variables: %s", eval_variables)

        rendered = rendered.replace("{% slot %}", page["_content"])

        for_match = FOR_REGEX.search(rendered)
        loop_end = END_REGEX.search(rendered, for_match.end())
        while for_match:
            if not loop_end:
                raise ValueError(
                    "No end found for for loop starting at", for_match.group(0)
                )
            logging.debug("Rendering for loop %s", for_match.group(0))
            var = for_match.group("var")
            iterable = for_match.group("iter")
            loop_content = rendered[for_match.end(): loop_end.start()]
            logging.debug("Loop content: %s", loop_content)

            rendered_loop = ""
            logging.debug("Looping over %s", eval(iterable, eval_variables))
            for item in eval(iterable, eval_variables):
                current_loop_render = loop_content
                m = VARIABLE_REGEX.search(current_loop_render)
                while m:
                    logging.debug(
                        "Rendering possibly loop variable %s", m.group(0)
                    )

                    e = eval(m.group("var"), eval_variables, {var: item})
                    logging.debug("Replacing %s with %s", m.group(0), e)

                    current_loop_render = current_loop_render.replace(
                        m.group(0), e
                    )
                    m = VARIABLE_REGEX.search(current_loop_render)
                rendered_loop += current_loop_render
            logging.debug("Rendered loop: %s", rendered_loop)
            rendered = (
                rendered[: for_match.start()]
                + rendered_loop
                + rendered[loop_end.end():]
            )

            for_match = FOR_REGEX.search(rendered, loop_end.end())
            if for_match:
                loop_end = END_REGEX.search(rendered, for_match.end())

        var = VARIABLE_REGEX.search(rendered)
        while var:
            logging.debug("Rendering non-loop variable %s", var.group(0))
            e = eval(var.group("var"), eval_variables)
            logging.debug("Replacing %s with %s", var.group(0), e)
            rendered = rendered.replace(var.group(0), e)
            var = VARIABLE_REGEX.search(rendered)

        if rendered.find(r"{%") != -1:
            raise ValueError("Unresolved variable in layout.")

        return rendered
