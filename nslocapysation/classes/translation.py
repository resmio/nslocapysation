__author__ = 'JanNash'



class Translation(object):
    """
    A class whose instances represent complete translations (with optional comments)
    as they can be found in .strings-localization-files.
    """
    ### INITIALIZER ###

    def __init__(self, language_code, comment, key, translation):

        if key is None:
            raise ValueError('Tried to create an instance of Translation with None as key! '
                             'This is likely a programming-error in nslocapysation :(')
        if translation is None:
            raise ValueError('Tried to create an instance of Translation with None as translation. '
                             'Instead, an instance of IncompleteTranslation should be created. '
                             'This is likely a programming-error in nslocapysation :(')

        self._language_code = language_code
        self._comment = comment
        self._key = key
        self._translation = translation

    ### MAGIC ###

    def __str__(self):
        result = ''
        has_comment = self.comment is not None
        if has_comment:
            result += '\n' + self.comment + '\n'
        result += ('"{key}" = "{translation}";'
                   ''.format(key=self.key,
                             translation=self.translation))
        if has_comment:
            result += '\n'
        return result

    def __hash__(self):
        return (hash(self.language_code) ^
                hash(self.comment) ^
                hash(self.key) ^
                hash(self.translation))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.language_code == other.language_code and
                self.key == other.key and
                self.translation == other.translation)

    def __ne__(self, other):
        return not self.__eq__(other=other)

    ### PROPERTIES ###

    @property
    def language_code(self):
        return self._language_code

    @property
    def comment(self):
        return self._comment

    @property
    def key(self):
        return self._key

    @property
    def translation(self):
        return self._translation

