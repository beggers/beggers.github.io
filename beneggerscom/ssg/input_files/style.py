from beneggerscom.ssg.input_files import InputFile


class StyleFile(InputFile):
    name: str
    content: str

    @classmethod
    def from_lines(cls, name: str, lines: list[str]):
        style_file = StyleFile()
        style_file.name = name
        style_file.content = "\n".join(lines)
        return style_file
