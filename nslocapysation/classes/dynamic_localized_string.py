__author__ = 'JanNash'

from nslocapysation.classes.localized_string import LocalizedString


class DynamicLocalizedString(LocalizedString):
    """
    A subclass of LocalizedString, whose instances represent
    localized strings that are used with a dynamic key
    (i.e. some variable as key).
    Those are special because you need to check that there is a
    localization for every possible value of the variable.
    """
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return (self.key == other.key and
                self.full_sourcefile_path == other.full_sourcefile_path and
                self.sourcefile_line_number == other.sourcefile_line_number and
                self.line_occurrence_number == other.line_occurrence_number)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return (hash(self.key) ^
                hash(self.sourcefile_line_number) ^
                hash(self.line_occurrence_number) ^
                hash(self.full_sourcefile_path))