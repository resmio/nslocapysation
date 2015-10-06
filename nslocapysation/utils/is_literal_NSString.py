__author__ = 'JanNash'


def is_literal_NSString(strng):
    return strng[0:2] == '@"' and strng[-1] == '"'