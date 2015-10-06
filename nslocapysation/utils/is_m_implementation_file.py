__author__ = 'JanNash'

import os


def is_m_implementation_file(path):
    return os.path.splitext(path)[1] == '.m'