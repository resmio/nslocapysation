__author__ = 'JanNash'

import os
import logging
from nslocapysation import constants
from nslocapysation.utils.is_m_implementation_file import is_m_implementation_file
from nslocapysation.utils.is_lproj_localization_file import is_lproj_localization_file


def collect_m_and_lproj_file_paths(project_source_root_path):
    """
    Walks the given project_source_root_path and returns a dictionary containing:
        {'m_file_paths': [a list of paths to .m-implementation-files],
         'lproj_file_paths': [a list of paths to .lproj-localization-files]

    :param project_source_root_path: The source root-path of your Xcode project that should be crawled.
    :returns: A dictionary containing lists of file-paths as values.

    :type: str
    :rtype: dict[str, list[str]]
    """
    logging.info('Searching {project_source_root_path} for .m-implementation-files and .lproj-localization-files.')

    result = {constants.M_FILE_PATHS_KEY: [],
              constants.LPROJ_FILE_PATHS_KEY: []}

    num_of_m_implementation_files = 0
    num_of_lproj_localization_files = 0

    for dir_path, subdir_names, files in os.walk(project_source_root_path):
        for file_ in files:
            if is_m_implementation_file(file_):
                file_path = os.path.join(dir_path, file_)
                result[constants.M_FILE_PATHS_KEY].append(file_path)
                num_of_m_implementation_files += 1
                logging.debug("Found implementation-file '{file_}' at path '{dir_path}'"
                              "".format(file_=file_,
                                        dir_path=dir_path))
            elif is_lproj_localization_file(file_):
                file_path = os.path.join(dir_path, file_)
                result[constants.LPROJ_FILE_PATHS_KEY].append(file_path)
                num_of_lproj_localization_files += 1
                logging.debug("Found localization-file '{file_}' at path '{dir_path}'"
                              "".format(file_=file_,
                                        dir_path=dir_path))

    logging.info('Found {num} implementation-files.'
                 ''.format(num=num_of_m_implementation_files))
    logging.info('Found {num} localization-files.'
                 ''.format(num=num_of_lproj_localization_files))
    return result