__author__ = 'JanNash'

import os


def is_lproj_localization_file(path):
    return os.path.splitext(path)[1] == '.lproj'