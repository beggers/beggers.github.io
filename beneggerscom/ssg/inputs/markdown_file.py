from beneggerscom.ssg.inputs import InputFile

import logging


class MarkdownFile(InputFile):
    title: str = ""
    date: str = ""
    meta_title: str = ""
    description: str = ""
    content: str = ""

    def from_markdown(
        self, lines: list[str], base_site_title: str = "Ben Eggers dot com"
    ):
        logging.debug("Read lines %s", lines)
        if lines[0].strip() != "---":
            raise ValueError("Lines do not begin with metadata marker (---).")

        metadata_end = 0
        for i, line in enumerate(lines[1:]):
            if line.strip().startswith("---"):
                # We start at 1 so we need to add 1
                metadata_end = i + 1
                break
            key, value = line.split(":")
            self._set_metadata_item(key.strip().lower(), value.strip())
        logging.debug("Metadata ends at line %d", metadata_end + 1)
        logging.debug("Self after metadata ingest: %s", self)

        # Add one because the start index is inclusive
        self.content = "\n".join(lines[metadata_end + 1 :])

        if not self.title:
            raise ValueError(f"No title for file. Parsed {self}")
        if not self.meta_title:
            self.meta_title = self.title
            if base_site_title:
                self.meta_title = self.meta_title + " | " + base_site_title

    def _set_metadata_item(self, key: str, value: str):
        if key == "title":
            self.title = value.title()
        elif key == "date":
            self.date = value
        elif key == "description":
            self.description = value
        elif key == "meta_title":
            self.meta_title = value
        else:
            raise ValueError(f"Unknown metadata key: {key}")


class LayoutFile(InputFile):
    name: str
    content: str


class StaticFile(InputFile):
    # We don't need to store content -- we'll just copy all statics
    # into the output directory on render.
    pass


class StyleFile(InputFile):
    name: str
    content: str
