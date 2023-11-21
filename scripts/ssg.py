"""
A simple static site generator to make the site. MUST be run from the top-
level directory.

Notes:
- Errors if there are multiple definitions for the same output resource.
- Variables available to templates:
  - `page`: The page being rendered, including metadata.
  - `pages`: A list of all pages, including metadata.
  - `site`: A dictionary of site metadata.
"""


import argparse
import json
import logging
import os
import re
import shutil

import markdown


CONFIG_FILE = "config.json"
LAYOUTS_DIR = "layouts"
PAGES_DIR = "pages"
STATIC_DIR = "static"
STYLE_DIR = "styles"

# I should really use a CSS templater/renderer, but this does everything I need.
# Same with HTML. Plus it was fun to write!
CSS_IMPORT_REGEX = re.compile(r"@import '(?P<file>.+?)';")
END_REGEX = re.compile(r"{% end %}")
FOR_REGEX = re.compile(r"{% for (?P<var>.+?) in (?P<iter>.+?) %}")
LAYOUT_DEF_REGEX = re.compile(r"{% define (?P<layout>.+?) %}")
LAYOUT_END_REGEX = re.compile(r"{% end (?P<layout>.+?) %}")
LAYOUT_INCLUDE_REGEX = re.compile(r"{% include (?P<layout>.+?) %}")
VARIABLE_REGEX = re.compile(r"{% (?P<var>.+?) %}")

DEFAULT_DESCRIPTION = "No description specified for this page, sorry!"


class SiteGenerator:
    def __init__(
        self, hostname, title, description, protocol, default_layout, default_style
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

        self.static_dir = None
        self.statics = []

        self.markdown_dir = None
        self.markdowns = {}

        self.layouts_dir = None
        self.layouts = {}
        self.partials = {}

        self.styles_dir = None
        self.styles = {}
        self.rendered_styles = {}

    def ingest_markdown_directory(self, path):
        logging.info("Ingesting markdown directory %s", path)
        self.markdown_dir = path
        files = self._all_files_in_dir(path)
        for f in files:
            logging.debug("Ingesting markdown file %s", f)
            self._ingest_md_file(f)

    def _ingest_md_file(self, path):
        if path in self.markdowns:
            raise ValueError("Markdown file already ingested.")
        if not path.endswith(".md"):
            raise ValueError("Markdown file {} does not end with .md.".format(path))

        with open(path, "r") as f:
            lines = f.readlines()
        logging.debug("Read lines %s", lines)
        if lines[0].strip() != "---":
            raise ValueError(
                "Markdown file {} does not begin with metadata.".format(path)
            )

        page_data = {}
        metadata_end = 0
        for i, line in enumerate(lines[1:]):
            if line.strip() == "---":
                metadata_end = i
                break
            key, value = line.split(":")
            page_data[key.strip().lower()] = value.strip()
        logging.debug("Metadata ends at line %d", metadata_end + 1)
        logging.debug("Metadata: %s", page_data)

        content = self._md_to_html(lines[metadata_end + 1 :])
        page_data["_content"] = content

        if path == os.path.join(self.markdown_dir, "index.md"):
            page_data["description"] = self.site_config["description"]
            page_data["title"] = self.site_config["title"]
            page_data["meta_title"] = self.site_config["title"]
        else:
            if "title" not in page_data or not page_data["title"]:
                page_data["title"] = (
                    os.path.basename(path).replace(".md", "").replace("-", " ").title()
                )
                logging.warning("No title specified for %s", path)
            page_data["meta_title"] = (
                page_data["title"] + " | " + self.site_config["title"]
            )
            if "description" not in page_data or not page_data["description"]:
                page_data["description"] = DEFAULT_DESCRIPTION
            logging.debug("Page description: %s", page_data["description"])

        url = path.replace(self.markdown_dir, "")[:-3].split("/")
        if url[-1] == "index":
            url = url[:-1]
        url.reverse()
        url = ".".join(url) + self.site_config["url"]
        if len(url) > 255:
            raise ValueError(f"URL too long. {url}")
        page_data["url"] = self.site_config["protocol"] + "://" + url
        logging.debug("Page URL: %s", page_data["url"])

        self.markdowns[path] = page_data

    def _md_to_html(self, lines):
        return markdown.markdown("".join(lines)).replace("<hr />", "")

    def ingest_layouts_directory(self, path):
        logging.info("Ingesting layouts directory %s", path)
        self.layouts_dir = path
        files = self._all_files_in_dir(path)
        for f in files:
            logging.debug("Ingesting layout file %s", f)
            self._ingest_layout_file(f)

    def _ingest_layout_file(self, path):
        if path in self.layouts:
            raise ValueError("Layout file already ingested.")

        with open(path, "r") as f:
            lines = f.readlines()
        logging.debug("Read lines %s", lines)

        # A layout is always either a page or a single named template.
        start_match = LAYOUT_DEF_REGEX.match(lines[0])
        if start_match:
            logging.debug("Layout is a named template: %s", start_match.group("layout"))
            partial_name = start_match.group("layout")
            end_match = LAYOUT_END_REGEX.match(lines[-1])
            if not end_match:
                raise ValueError("Layout definition does not end correctly.")
            if end_match.group("layout") != partial_name:
                raise ValueError("Layout name does not match end.")

            content = "".join(lines[1:-1])
            self.partials[partial_name] = content
            logging.debug("Partial content: %s", content)
        else:
            content = "".join(lines)
            self.layouts[os.path.basename(path)] = content
            logging.debug("Layout content: %s", content)

    def ingest_static_directory(self, path):
        logging.info("Ingesting static directory %s", path)
        self.static_dir = path
        self.statics = self._all_files_in_dir(path)
        logging.debug("Static files: %s", self.statics)

    def ingest_styles_directory(self, path):
        self.styles_dir = path
        files = self._all_files_in_dir(path)
        for f in files:
            self._ingest_style_file(f)

    def _ingest_style_file(self, path):
        if not path.endswith(".css"):
            raise ValueError("Style file {} does not end with .css.".format(path))
        with open(path, "r") as f:
            lines = f.readlines()
        logging.debug("Read lines %s", lines)
        self.styles[path.replace(self.styles_dir + "/", "")] = "".join(lines)

    def render(self, path):
        logging.info("Rendering site to %s", path)
        print(self.layouts.keys())
        if not self.static_dir:
            raise ValueError("No static directory set.")
        if not self.markdown_dir:
            raise ValueError("No markdown directory set.")
        if not self.layouts_dir:
            raise ValueError("No layouts directory set.")
        if not self.styles_dir:
            raise ValueError("No styles directory set.")

        for static in self.statics:
            logging.debug("Copying static file %s", static)
            shutil.copy(static, static.replace(self.static_dir, path))

        for style_path, style in self.styles.items():
            logging.debug("Rendering style %s", style)
            rendered = style
            match = CSS_IMPORT_REGEX.search(rendered)
            while match:
                logging.debug("Rendering import %s", match.group("file"))
                file = match.group("file")
                if file not in self.styles:
                    raise ValueError(f"Style '{file}' not found.")
                rendered = rendered.replace(match.group(0), self.styles[file])
                match = CSS_IMPORT_REGEX.search(rendered)
            self.rendered_styles[style_path] = rendered

        for md_path, md in self.markdowns.items():
            logging.debug("Rendering markdown file %s", md_path)
            self._render_page(md_path, md, path)

    def _render_page(self, md_path, md, path):
        layout_name = md.get("layout", self.site_config["default_layout"])
        logging.debug("Rendering page with layout %s", layout_name)
        if layout_name not in self.layouts:
            raise ValueError(f"Layout '{layout_name}' not found.")
        layout = self.layouts[layout_name]

        rendered = self._render_layout(layout, md)

        output_path = md_path.replace(self.markdown_dir, path).replace(".md", ".html")
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

        include = LAYOUT_INCLUDE_REGEX.search(rendered)
        while include:
            logging.debug("Rendering include %s", include.group("layout"))
            partial_name = include.group("layout")
            if partial_name not in self.partials:
                raise ValueError(f"Partial '{partial_name}' not found.")
            rendered = rendered.replace(include.group(0), self.partials[partial_name])
            include = LAYOUT_INCLUDE_REGEX.search(rendered)

        print(page["_content"])
        rendered = rendered.replace("{% slot %}", page["_content"])

        for_match = FOR_REGEX.search(rendered)
        loop_end = END_REGEX.search(rendered, for_match.end())
        while for_match:
            logging.debug("Rendering for loop %s", for_match.group(0))
            if not loop_end:
                raise ValueError(
                    "No end found for for loop starting at", for_match.start()
                )
            var = for_match.group("var")
            iterable = for_match.group("iter")
            loop_content = rendered[for_match.end() : loop_end.start()]
            logging.debug("Loop content: %s", loop_content)

            rendered_loop = ""
            logging.debug("Looping over %s", eval(iterable, eval_variables))
            for item in eval(iterable, eval_variables):
                current_loop_render = loop_content
                m = VARIABLE_REGEX.search(current_loop_render)
                while m:
                    logging.debug("Rendering possibly loop variable %s", m.group(0))

                    e = eval(m.group("var"), eval_variables, {var: item})
                    logging.debug("Replacing %s with %s", m.group(0), e)

                    current_loop_render = current_loop_render.replace(m.group(0), e)
                    m = VARIABLE_REGEX.search(current_loop_render)
                rendered_loop += current_loop_render
            logging.debug("Rendered loop: %s", rendered_loop)
            rendered = (
                rendered[: for_match.start()]
                + rendered_loop
                + rendered[loop_end.end() :]
            )

            rendered = rendered.replace(for_match.group(0), "")
            rendered = rendered.replace(loop_end.group(0), "")
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

    def _all_files_in_dir(self, path):
        files = []
        for root, _, fs in os.walk(path):
            for f in fs:
                files.append(os.path.join(root, f))
        return files


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dev",
        help="Build for development instead of production.",
        action="store_true",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = json.load(open("config.json", "r"))
    logging.basicConfig(level=config.get("log_level", "INFO"))

    host = (
        config["dev_hostname"] + ":" + str(config["dev_port"])
        if args.dev
        else config["prod_hostname"]
    )
    protocol = "http" if args.dev else "https"
    generator = SiteGenerator(
        host,
        config["site_title"],
        config["site_description"],
        protocol,
        config["default_layout"],
        config["default_style"],
    )

    generator.ingest_markdown_directory(PAGES_DIR)
    generator.ingest_layouts_directory(LAYOUTS_DIR)
    generator.ingest_static_directory(STATIC_DIR)
    generator.ingest_styles_directory(STYLE_DIR)

    generator.render(config["content_dir"])


if __name__ == "__main__":
    main()
