__author__ = 'JanNash'

import re


def get_language_code_from_file_path(path):
    """
    Retrieves the language code from the path of a localization-file by using a regex.

    :param path: str
    :returns: The language code of the file.

    :type path: str
    :rtype: str
    """
    # Attention, this regex only works under os's with a slash separated path
    # but why should it work elsewhere anyway :D
    # One could of course use os.path.sep...
    RE_PATH = re.compile(r'([^\/]*?).lproj')
    result = RE_PATH.findall(path)
    if len(result) != 1:
        raise RuntimeError('Found multiple language-codes inside one file-path. Either there is something strange '
                           'with the project-structure or this is a programming-error in nslocapysation :/')
    else:
        return result[0]