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
    if len(result) > 1:
        raise RuntimeError('Found multiple language-codes inside file-path {file_path}. '
                           'Either there is something strange with the project-structure or this is a '
                           'programming/regex-error in nslocapysation :/'
                           ''.format(file_path=path))
    elif len(result) == 0:
        raise RuntimeError('Found no language-codes inside file-path {file_path}. '
                           'Either there is something strange with the project-structure or this is a '
                           'programming/regex-error in nslocapysation :/'
                           ''.format(file_path=path))
    else:
        return result[0]