__author__ = 'JanNash'

import re
import logging
from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.translation import Translation

class LocalizableStringFile(object):
    """
    A class whose instances represent .lproj-localizable-string-files.
    """
    ### CLASS CONSTANTS ###

    RE_COMMENT = re.compile(r'\/\/(.*)')
    RE_TRANSLATION = re.compile(r'\"(.*?)\"\s*\=\s*\"(.*?)\"\;')

    ### INITIALIZER ###

    def __init__(self, language_code, file_path):
        self._language_code = language_code
        self._file_path = file_path

        self._translations = None

    ### PROPERTIES ###

    @property
    def language_code(self):
        return self._language_code

    @property
    def file_path(self):
        return self._file_path

    @property
    def translations(self):
        if self._translations is None:
            self._create_translations()
        return self._translations

    ### PRIVATE METHODS ###

    def _create_translations(self):
        result = set()

        logging.info('Creating localized strings for language_code {language_code}'
                     ''.format(language_code=self.language_code))
        logging.debug('Creating localized strings from file at path {path}'
                      ''.format(self.file_path))

        with open(self.file_path, mode='r') as file_:
            lines = file_.readlines()

        num_of_comments = 0
        num_of_translations = 0

        comment = None
        translation = None
        for line in lines:
            if comment is None:
                comment = self.RE_COMMENT.match(line)
            if comment is not None:
                num_of_comments += 1
                logging.debug('Found comment: {comment}'
                              ''.format(comment=comment))
                continue
            translation = self.RE_TRANSLATION.match(line)
            if translation is not None:
                num_of_translations += 1
                logging.debug('Found translation: {translation}'
                              ''.format(translation=translation))
                # result.add(Translation(language_code=self.language_code,
                #                        comment=comment,
                #                        key=translation[0],
                #                        translation=translation[1]))
                translation = None
                comment = None


        self._translations = result

    ### PUBLIC METHODS ###

    def has_translation_for_localized_string(self, localized_string):
        return



