import os


def is_implementation_file(path):
    return os.path.splitext(path)[1] in ['.m', '.swift']
