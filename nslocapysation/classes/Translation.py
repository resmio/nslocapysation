__author__ = 'JanNash'



class Translation(object):
    """
    A class whose instances represent translations (with optional comments)
    as they can be found in .lproj-localization-files.
    """
    ### INITIALIZER ###

    def __init__(self, language_code, comment, key, translation):
        self._language_code = language_code
        self._comment = comment
        self._key = key
        self._translation = translation

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

