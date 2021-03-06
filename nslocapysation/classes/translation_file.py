import re
import os
import shutil
import datetime
import logging
import itertools
from nslocapysation import constants
from nslocapysation.utils.n_ import n_
from nslocapysation.utils.num_of_words_in_string import num_of_words_in_string
from nslocapysation.classes.translation import Translation
from nslocapysation.classes.incomplete_translation import IncompleteTranslation


class TranslationFile(object):
    """
    A class whose instances represent .strings-localizable-string-files.
    """
    # CLASS CONSTANTS #

    RE_COMMENT = re.compile(r'\/\/(?P<comment>.*)')
    RE_TRANSLATION = re.compile(r'\"(?P<key>.*?)\"\s*\=\s*\"(?P<translation>.*?)\"\;')
    RE_INCOMPLETE_TRANSLATION = re.compile(r'\"(?P<key>.*?)\"\s*\=\s*\Z')

    # INITIALIZER #

    def __init__(self, language_code, file_path):
        self._language_code = language_code
        self._file_path = file_path

        self._translations = None
        self._incomplete_translations = None

    # PROPERTIES #

    @property
    def language_code(self):
        return self._language_code

    @property
    def file_path(self):
        return self._file_path

    @property
    def translations(self):
        if self._translations is None:
            self._collect_translations()
        return self._translations

    @property
    def incomplete_translations(self):
        if self._incomplete_translations is None:
            self._collect_translations()
        return self._incomplete_translations

    # PRIVATE METHODS #

    def _collect_translations(self):
        translations = set()
        incomplete_translations = set()

        logging.info('Collecting Translations for language_code {language_code}'
                     ''.format(language_code=self.language_code))
        logging.debug('Collecting Translations from file at path {file_path}'
                      ''.format(file_path=os.path.abspath(self.file_path)))

        with open(self.file_path, mode='r') as file_:
            lines = file_.readlines()

        num_of_comments = 0
        num_of_translations = 0
        num_of_incomplete_translations = 0

        comment = None
        for line in lines:
            comment_match = self.RE_COMMENT.match(line)
            translation_match = self.RE_TRANSLATION.match(line)
            incomplete_translation_match = self.RE_INCOMPLETE_TRANSLATION.match(line)

            if comment_match is not None:
                # Supporting multi-line comments
                if comment is None:
                    comment = comment_match.group()
                else:
                    comment += '\n' + comment_match.group()
                continue
            elif translation_match is not None:
                num_of_translations += 1

                if comment is not None:
                    num_of_comments += 1

                key = translation_match.group(constants.KEY_KEY)
                translation = translation_match.group(constants.TRANSLATION_KEY)
                translations.add(Translation(language_code=self.language_code,
                                             comment=comment,
                                             key=key,
                                             translation=translation))
                comment = None
            elif incomplete_translation_match is not None:
                num_of_incomplete_translations += 1

                if comment is not None:
                    num_of_comments += 1

                key = incomplete_translation_match.group(constants.KEY_KEY)
                incomplete_translations.add(IncompleteTranslation(language_code=self.language_code,
                                                                  comment=comment,
                                                                  key=key))
                comment = None

        logging.info('Found {num} comments.'
                     ''.format(num=num_of_comments))
        logging.debug('Comments: {comments}'
                      ''.format(comments=[trans.comment for trans in translations if trans.comment is not None]))
        logging.info('Found {num} translations.'
                     ''.format(num=num_of_translations))

        logging.debug('Translations:')
        for translation in translations:
            logging.debug('    {transl}'
                          ''.format(transl=translation))

        if num_of_incomplete_translations > 0:
            logging.warning('Found {num} incomplete translations.'
                            ''.format(num=num_of_incomplete_translations))
            logging.warning('Incomplete translations: {translations}'
                            ''.format(translations=[str(trans) for trans in incomplete_translations]))
        else:
            logging.info('Found 0 incomplete translations.')

        self._translations = translations
        self._incomplete_translations = incomplete_translations

    def _create_backup_file(self):
        now = datetime.datetime.now()
        now_string = now.strftime('%d%m%Y_%Hh%Mm%Ss')
        path_wo_ext = os.path.splitext(self.file_path)[0]
        backup_file_path = (path_wo_ext + '_' + now_string + '.bak')
        i = 2
        while os.path.exists(backup_file_path):
            backup_file_path = (path_wo_ext + '_' + now_string + str(i) + '_' + '.bak')
            i += 1

        logging.info('Creating backup of file {file_} for language-code {language_code} => {backup_file}'
                     ''.format(file_=os.path.basename(self.file_path),
                               language_code=self.language_code,
                               backup_file=os.path.basename(backup_file_path)))

        logging.debug('Full backup-file-path: {file_path}'
                      ''.format(file_path=os.path.abspath(backup_file_path)))

        shutil.copy(self.file_path, backup_file_path)

    # PUBLIC METHODS #

    def has_translation_for_localized_string(self, localized_string):
        """
        Checks if a localized string has a translation in this file

        :param localized_string: The localized string to search for.
        :returns: True if there is a complete translation for the string.

        :type localized_string: LocalizedString
        :rtype: bool
        """
        for translation in self.translations:
            if translation.key == localized_string.key:
                return True
        return False

    def add_incomplete_translation(self, incomplete_translation):
        """
        Adds an instance of IncompleteTranslation to the files incomplete translations.

        :param incomplete_translation: The incomplete translation to add.

        :type incomplete_translation: IncompleteTranslation
        """
        self._incomplete_translations.add(incomplete_translation)

    def write_file(self):
        """
        Creates a backup-file and writes all translations back to its file-path.
        """
        self._create_backup_file()

        logging.info('Writing translations of language_code {language_code} to file {file_}'
                     ''.format(language_code=self.language_code,
                               file_=os.path.basename(self.file_path)))

        all_translations = list(self.translations) + list(self.incomplete_translations)

        def sorting_func(translation):
            return num_of_words_in_string(translation.key), translation.key.lower()

        sorted_translations = sorted(
            all_translations,
            key=sorting_func)

        stringified_translations = []

        def grouping_func(translation):
            return num_of_words_in_string(translation.key)

        for length, group in itertools.groupby(
                sorted_translations,
                key=grouping_func):
            stringified_translations.append('\n/* {num} {n_words} */'
                                            ''.format(num=length,
                                                      n_words=n_(length, 'word')))
            stringified_translations += [str(trans) for trans in group]

        content = '\n'.join(stringified_translations)
        content += '\n'
        with open(self.file_path, mode='w') as outfile:
            outfile.write(content)
