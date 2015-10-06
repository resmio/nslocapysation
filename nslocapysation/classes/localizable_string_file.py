__author__ = 'JanNash'

import re
import os
import logging
from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.translation import Translation


class LocalizableStringFile(object):
    """
    A class whose instances represent .lproj-localizable-string-files.
    """
    ### CLASS CONSTANTS ###

    RE_COMMENT = re.compile(r'\/\/(?P<comment>.*)')
    RE_TRANSLATION = re.compile(r'\"(?P<key>.*?)\"\s*\=\s*\"(?P<translation>.*?)\"\;')

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
            self._collect_translations()
        return self._translations

    ### PRIVATE METHODS ###

    def _collect_translations(self):
        result = set()

        logging.info('Collecting Translations for language_code {language_code}'
                     ''.format(language_code=self.language_code))
        logging.debug('Collecting localized strings from file at path {file_path}'
                      ''.format(file_path=os.path.abspath(self.file_path)))

        with open(self.file_path, mode='r') as file_:
            lines = file_.readlines()

        num_of_comments = 0
        num_of_translations = 0

        comment = None
        for line in lines:
            comment_match = self.RE_COMMENT.match(line)
            translation_match = self.RE_TRANSLATION.match(line)

            if comment_match is not None:
                # Supporting multi-line comments
                if comment is None:
                    comment = comment_match.group()
                else:
                    comment += '\n' + comment_match.group()
                continue
            elif translation_match is not None:
                translation = translation_match.group(0, 1)
                num_of_translations += 1

                if comment is not None:
                    num_of_comments += 1
                    logging.debug('Found comment: {comment}'
                                  ''.format(comment=comment))

                logging.debug('Found translation: {translation}'
                              ''.format(translation=translation))
                result.add(Translation(language_code=self.language_code,
                                       comment=comment,
                                       key=translation[0],
                                       translation=translation[1]))
                translation = None
                comment = None

        logging.info('Found {num} comments.'
                     ''.format(num=num_of_comments))
        logging.debug('Comments: {comments}'
                      ''.format(comments=[trans.comment for trans in result]))
        logging.info('Found {num} translations.'
                     ''.format(num=num_of_translations))
        logging.debug('Translations: {translations}'
                      ''.format(translations=[(trans.key, trans.translation) for trans in result]))

        self._translations = result

    ### PUBLIC METHODS ###

    def has_translation_for_localized_string(self, localized_string):
        return



