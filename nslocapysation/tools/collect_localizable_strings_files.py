__author__ = 'JanNash'

import os
from nslocapysation import constants
from nslocapysation.classes.localizable_string_file import LocalizableStringFile
from nslocapysation.utils.get_language_code_from_file_path import get_language_code_from_file_path


def collect_localizable_strings_files(localization_dir_paths):
    """
    Collects all localizations from the given localization_dir_paths and
    returns a list containing all localization-files parsed to LocalizableStringFile-instances.

    :param localization_dir_paths: The file-paths to the localization-dirs
                                   which contain the .strings-files that should be parsed.
    :returns: A list of LocalizableStringFile-instances..

    :type localization_dir_paths: list[str]
    :rtype: set[LocalizableStringFile]
    """
    result = set()
    for dir_path in localization_dir_paths:
        strings_file_path = os.path.join(dir_path, constants.LOCALIZABLE_STRINGS_FILE_NAME)
        language_code = get_language_code_from_file_path(strings_file_path)
        result.add(LocalizableStringFile(language_code=language_code,
                                         file_path=strings_file_path))
    return result