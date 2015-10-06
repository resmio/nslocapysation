__author__ = 'JanNash'

from nslocapysation.classes.localizable_string_file import LocalizableStringFile


COMMENT_KEY = 'comment'
LOCALIZATION_KEY = 'localization'

def collect_localizations(localization_file_paths):
    """
    Collects all localizations from the given localization_file_paths and
    returns a list containing all localization-files parsed to LocalizableStringFile-instances.

    :param localization_file_paths: The file-paths to the localization-files that should be parsed.
    :returns: A list of LocalizableStringFile-instances..

    :type localization_file_paths: list[str]
    :rtype: LocalizableStringFile
    """

