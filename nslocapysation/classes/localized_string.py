__author__ = 'JanNash'

import os


class LocalizedString(object):
    """
    A class whose instances represent occurrences of 'NSLocalizedString()' (or custom macros, like 'NSL()').
    """
    ### INITIALIZER ###
    def __init__(self,
                 macro=None,
                 key="",
                 comment=None,
                 translations=None,
                 full_sourcefile_path="",
                 sourcefile_line_number=None,
                 line_occurrence_index=None):

        self._macro = macro
        self._key = key
        self._comment = comment
        self._full_sourcefile_path = full_sourcefile_path
        self._sourcefile_line_number = sourcefile_line_number
        self._line_occurrence_index = line_occurrence_index

    ### MAGIC ###

    def __repr__(self):
        return ("[{class_name}]\n"
                "    macro:                     {macro}\n"
                "    key:                       {key}\n"
                "    comment:                   {comment}\n"
                "    sourcefile_name:           {sourcefile_name}\n"
                "    sourcefile_line_number:    {sourcefile_line_number}\n"
                "    line_occurrence_index:     {line_occurrence_index}\n"
                "    full_sourcefile_path:      {full_sourcefile_path}\n"
                "".format(class_name=self.__class__.__name__,
                          macro=self.macro,
                          key=self.key,
                          comment=self.comment,
                          sourcefile_name=self.sourcefile_name,
                          sourcefile_line_number=self.sourcefile_line_number,
                          line_occurrence_index=self.line_occurrence_index,
                          full_sourcefile_path=self.full_sourcefile_path))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.key != other.key:
            return False
        if self.key == other.key:
            if self.comment in [None, 'nil']:
                return True
            if other.comment in [None, 'nil']:
                return True
            if self.comment == other.comment:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.key)

    ### PROPERTIES ###

    @property
    def macro(self):
        return self._macro

    @property
    def key(self):
        return self._key

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, new_comment):
        if new_comment == 'nil':
            self._comment = None
        else:
            self._comment = new_comment

    @property
    def sourcefile_name(self):
        return os.path.basename(self.full_sourcefile_path)

    @property
    def sourcefile_line_number(self):
        return self._sourcefile_line_number

    @property
    def line_occurrence_index(self):
        return self._line_occurrence_index

    @property
    def full_sourcefile_path(self):
        return self._full_sourcefile_path