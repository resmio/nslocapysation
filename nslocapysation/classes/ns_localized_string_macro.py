import re


class NSLocalizedStringMacro(object):
    """
    A class whose instances represent a NSLocalizedString-macro with a certain format.
    This given format must include 'key' and can optionally contain 'comment'.
    The class the provides a compiled regex that can be used to search files.
    """
    # CLASS CONSTANTS #

    _KEY_FORMAT = r'key'
    _COMMENT_FORMAT = r'comment'

    _OBJC_KEY = r'\@\"key\"'
    _SWIFT_KEY = r'\"key\"'

    _OBJC_COMMENT = r'\@\"comment\"'
    _SWIFT_COMMENT = r'\"comment\"'

    _REPLACER = r'(.*?\W*?)'

    # INITIALIZER #

    def __init__(self, format_):

        if format_.find(self._KEY_FORMAT) == -1:
            raise ValueError(
                'Tried to create an instance of NSLocalizedStringMacro with format '
                '"{format_}", which is missing KEY_FORMAT "{key_format}"!'
                ''.format(format_=format_, key_format=self._KEY_FORMAT)
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
        return self.format_.find(self._COMMENT_FORMAT) != -1

    # METHODS #

    def get_regex(self, is_objc_file):
        key_ = self._OBJC_KEY if is_objc_file else self._SWIFT_KEY

        # Escape all metas
        escaped_format = re.escape(self.format_)
        regex_string = escaped_format.replace(key_, self._REPLACER)

        if self.has_comment:
            comment_ = self._OBJC_COMMENT if is_objc_file else self._SWIFT_COMMENT
            regex_string = regex_string.replace(comment_, self._REPLACER)

        return re.compile(regex_string)
