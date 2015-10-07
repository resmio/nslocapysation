__author__ = 'JanNash'

import os
import logging
from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.incomplete_translation import IncompleteTranslation
from nslocapysation.classes.translation_file import TranslationFile


def check_localizations(translation_files, localized_strings, update=False):
    """
    This function checks for each localized-string if it has a translation in every language.
    If a translation is missing, it logs a warning.
    If update is set to True, it also adds an empty translation, which will look like this:
        '"key" ='
    This will lead to a compile error in Xcode, so you might want to set update when you build a release version
    of your App, which will prevent you from accidentally releasing an App with missing localizations.

    :param translation_files: A set containing all TranslationFile-instances against which the
                              given localized_strings should be checked.
    :param localized_strings: A set containing all LocalizedStrings that should be checked against the
                              TranslationFile-instances.
    :param update: If set to True, the keys of missing translations will be written to the files.
                   If set to False, only warnings will be logged on missing translations.
    :returns: Nothing.

    :type translation_files: set[TranslationFile]
    :type localized_strings: set[LocalizedString]
    """
    for file_ in translation_files:
        for loc_string in localized_strings:
            if not file_.has_translation_for_localized_string(loc_string):
                logging.warning("File {file_} missing translation for key '{key}'!"
                                "".format(file_=os.path.basename(file_.file_path),
                                          key=loc_string.key))
                if update:
                    inc_trans = IncompleteTranslation(language_code=file_.language_code,
                                                                   comment=loc_string.comment,
                                                                   key=loc_string.key)
                    file_.add_incomplete_translation(inc_trans)

    if update:
        for file_ in translation_files:
            file_.create_backup_file()
            file_.write_file()