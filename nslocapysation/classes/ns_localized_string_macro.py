import re


class NSLocalizedStringMacro(object):
    """
    A class whose instances represent a NSLocalizedString-macro with a certain format.
    This given format must include 'key' and can optionally contain 'comment'.
    The class the provides a compiled regex that can be used to search files.
    """
    # CLASS CONSTANTS #

    KEY_FORMAT = r'key'
    COMMENT_FORMAT = r'comment'

    # INITIALIZER #

    def __init__(self, format_):

        if format_.find(self.KEY_FORMAT) == -1:
            raise ValueError(
                'Tried to create an instance of NSLocalizedStringMacro with format '
                '"{format_}", which is missing KEY_FORMAT "{key_format}"!'
                ''.format(format_=format_, key_format=self.KEY_FORMAT)
            )

        self._format_ = format_
        self._regex = None

    # MAGIC #

    def __repr__(self):
        return '"{}"'.format(self.format_)

    # READONLY PROPERTIES #

    @property
    def format_(self):
        return self._format_

    @property
    def has_comment(self):
        return self.format_.find(self.COMMENT_FORMAT) != -1

    # METHODS #

    def get_regex(self):
        # Escape all metas
        escaped_format = re.escape(self.format_)
        regex_string = escaped_format.replace(r'\@\"key\"', r'(.*?)')

        if self.has_comment:
            regex_string = regex_string.replace(r'\@\"comment\"', r'(.*?)')
        return re.compile(regex_string)
