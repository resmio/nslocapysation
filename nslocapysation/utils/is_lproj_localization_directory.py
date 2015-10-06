__author__ = 'JanNash'

import os
from nslocapysation import constants


def is_lproj_localization_directory(path):
    if os.path.splitext(path)[1] != '.lproj':
        return False
    supposed_path = os.path.join(path, constants.LOCALIZABLE_STRINGS_FILE_NAME)
    return os.path.exists(supposed_path) and os.path.isfile(supposed_path)