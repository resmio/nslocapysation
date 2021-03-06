import logging
from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.dynamic_localized_string import DynamicLocalizedString
from nslocapysation.classes.incomplete_translation import IncompleteTranslation
from nslocapysation.classes.translation_file import TranslationFile
from nslocapysation.utils.n_ import n_


def check_translations(translation_files, localized_strings, update=False, ignore_language_codes=()):
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
    :param ignore_language_codes: Language codes that should be ignored when detecting translations.
                                  This is needed when you
    :returns: Nothing.

    :type translation_files: set[TranslationFile]
    :type localized_strings: set[LocalizedString]
    """
    files_to_write = []

    for file_ in translation_files:
        if file_.language_code in ignore_language_codes:
            logging.info('Ignoring language-code "{language_code}"'
                         ''.format(language_code=file_.language_code))
            continue
        else:
            files_to_write.append(file_)

        missing_translation_strings = []
        for loc_string in localized_strings:
            if not isinstance(loc_string, DynamicLocalizedString):
                if not file_.has_translation_for_localized_string(loc_string):
                    missing_translation_strings.append(loc_string)

        logging.warning('Found {n} missing translations for language {lang_code}'
                        ''.format(n=len(missing_translation_strings),
                                  lang_code=file_.language_code))

        if missing_translation_strings:
            n_translation = n_(len(missing_translation_strings), 'translation')
            n_key = n_(len(missing_translation_strings), 'key')
            logging.warning('Language "{lang_code}" missing {n_translation} for {n_key} {keys}!'
                            ''.format(lang_code=file_.language_code,
                                      n_translation=n_translation,
                                      n_key=n_key,
                                      keys=[strng.key for strng in missing_translation_strings]))
            if update:
                for strng in missing_translation_strings:
                    inc_trans = IncompleteTranslation(language_code=file_.language_code,
                                                      comment=strng.comment,
                                                      key=strng.key)
                    file_.add_incomplete_translation(inc_trans)

    if update:
        for file_ in files_to_write:
            file_.write_file()
