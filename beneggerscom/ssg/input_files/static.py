from beneggerscom.ssg.input_files import InputFile


class StaticFile(InputFile):
    # We don't need to store content -- we'll just copy all statics
    # into the output directory on render.
    pass
