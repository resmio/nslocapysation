__author__ = 'JanNash'

from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.localizable_string_file import LocalizableStringFile


def check_localizations(localizable_strings_files, localized_strings, update=False):
    """
    This function checks for each localized-string if it has a translation in every language.
    If a translation is missing, it logs a warning.
    If update is set to True, it also adds an empty translation, which will look like this:
        '"key" ='
    This will lead to a compile error in Xcode, so you might want to set update when you build a release version
    of your App, which will prevent you from accidentally releasing an App with missing localizations.

    :param localizable_strings_files: A set containing all LocalizableStringFile-instances against which the
                                     given localized_strings should be checked.
    :param localized_strings: A set containing all LocalizedStrings that should be checked against the
                              LocalizableStringFile-instances.
    :param update: If set to True, the keys of missing translations will be written to the files.
                   If set to False, only warnings will be logged on missing translations.
    :returns: Nothing.

    :type localizable_strings_files: set[LocalizableStringFile]
    :type localized_strings: set[LocalizedString]
    """
    if update:


    pass

