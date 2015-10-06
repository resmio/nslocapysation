__author__ = 'JanNash'

import re
from nslocapysation import constants


class NSLocalizedStringMacro(object):
    """
    A class whose instances represent a NSLocalizedString-macro with a certain format.
    This given format must include 'key' and can optionally contain 'comment'.
    The class the provides a compiled regex that can be used to search files.
    """
    ### INITIALIZER ###

    def __init__(self, format_):

        if format_.find(constants.KEY_FORMAT) == -1:
            raise ValueError(
                "Tried to create an instance of NSLocalizedStringMacro with format "
                "'{format_}', which is missing KEY_FORMAT '{key_format}'!"
                "".format(format_=format_, key_format=constants.KEY_FORMAT)
            )

        self._format_ = format_
        self._regex = None

    ### MAGIC ###

    def __repr__(self):
        return "'{}'".format(self.format_)

    ### READONLY PROPERTIES ###

    @property
    def format_(self):
        return self._format_

    @property
    def has_comment(self):
        return self.format_.find(constants.COMMENT_FORMAT) != -1

    ### METHODS ###

    def getRegex(self):
        # Escape all metas
        escaped_format = re.escape(self.format_)
        regex_string = escaped_format.replace(r'\@\"key\"', r'(.*?)')

        if self.has_comment:
            regex_string = regex_string.replace(r'\@\"comment\"', r'(.*?)')
        return re.compile(regex_string)