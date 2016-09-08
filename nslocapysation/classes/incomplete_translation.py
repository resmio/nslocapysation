from nslocapysation.classes.translation import Translation


class IncompleteTranslation(Translation):
    """
    A class whose instances represent translations that are still to be done, i.e. a key and maybe a comment.
    When run.py is ran with --update set, those will be stringified and written to the .strings-files,
    which will then lead to a compile-error in Xcode, so you don't accidentally ship an App that's missing translations.
    """
    # INITIALIZER #

    def __init__(self, language_code, comment, key):
        super(IncompleteTranslation, self).__init__(language_code=language_code,
                                                    comment=comment,
                                                    key=key,
                                                    translation='')
        self._translation = None

    # MAGIC #

    def __str__(self):
        result = ''
        if self.comment is not None:
            result += self.comment + '\n'
        result += ('"{key}" = '
                   ''.format(key=self.key))
        return result
