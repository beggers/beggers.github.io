import os
import re
import shutil
from typing import Optional

from beneggerscom.utils.hostname import filename_to_url
from beneggerscom.ssg.input_files.markdown import MarkdownFile
from beneggerscom.ssg.input_files.layout import LayoutFile
from beneggerscom.ssg.input_files.style import StyleFile
from beneggerscom.ssg.page import Page

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
        # Style name -> materialized CSS suitable for direct inclusion in HTML
        self.materialized_styles: dict[str, str] = {}

        self.pages: list[Page] = []

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
            if not filename.endswith(".html"):
                raise ValueError(
                    "Layout file {} does not end with .html.".format(filename)
                )
            logging.debug("Ingesting layout file %s", filename)

            with open(filename, "r") as f:
                default_layout_name = os.path.basename(filename)
                layout = LayoutFile.from_lines(
                    default_layout_name, f.readlines()
                )
                if layout.partial:
                    if layout.name in self.partials:
                        raise ValueError("Partial layout already ingested.")
                    self.partials[layout.name] = layout
                else:
                    if layout.name in self.layouts:
                        raise ValueError("Layout already ingested.")
                    self.layouts[layout.name] = layout

    def ingest_static_directory(self, path: str) -> None:
        logging.info("Ingesting static directory %s", path)
        self.static_dir = path
        self.statics = self._all_files_in_dir(path)
        logging.debug("Static files: %s", self.statics)

    def ingest_styles_directory(self, path: str) -> None:
        logging.info("Ingesting styles directory %s", path)
        self.styles_dir = path
        files = self._all_files_in_dir(path)
        for filename in files:
            name = filename.replace(self.styles_dir + "/", "")
            if name in self.styles:
                raise ValueError("Style file already ingested.")
            if not filename.endswith(".css"):
                raise ValueError(
                    "Style file {} does not end with .css.".format(filename)
                )
            with open(filename, "r") as f:
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

        self._materialize_styles()
        self._render_pages(path)
        self._flush_pages()
        self._copy_statics(path)

    def _materialize_styles(self) -> None:
        for style_name, style in self.styles.items():
            self.materialized_styles[
                style_name
            ] = style.materialize(self.styles)

    def _copy_statics(self, path: str) -> None:
        if not self.static_dir:
            raise ValueError("No static directory set.")
        for static in self.statics:
            logging.debug("Copying static file %s", static)
            shutil.copy(static, static.replace(self.static_dir, path))

    def _render_pages(self, path: str) -> None:
        if not self.markdown_dir:
            raise ValueError("No markdown directory set.")
        # TODO this path and URL stuff is jacked
        for md_path, md in self.markdowns.items():
            logging.debug("Rendering markdown file %s", md_path)
            target_path = md_path.replace(
                self.markdown_dir,
                path
            ).replace(
                ".md", ".html"
            )
            page = Page(
                md=md,
                layout=self.layouts.get(
                    md.layout,
                    self.layouts[self.site_config['default_layout']]
                ),
                url=filename_to_url(
                    target_path.replace(path + "/", ""),
                    self.site_config["protocol"],
                    self.site_config["url"]
                ),
                # TODO allow configurable styles (mostly done already)
                style=self.materialized_styles[
                    self.site_config["default_style"]
                ],
                path=target_path,
            )
            self.pages.append(page)
        for page in self.pages:
            page.render(
                self.site_config["url"],
                self.site_config["protocol"],
                self.partials,
                self.pages,
            )

    def _flush_pages(self) -> None:
        for page in self.pages:
            page.flush()
