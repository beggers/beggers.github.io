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

from beneggerscom.ssg.site_generator import SiteGenerator


CONFIG_FILE = "config.json"
LAYOUTS_DIR = "layouts"
PAGES_DIR = "pages"
STATIC_DIR = "static"
STYLE_DIR = "styles"
DRAFTS_DIR = "drafts"


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
