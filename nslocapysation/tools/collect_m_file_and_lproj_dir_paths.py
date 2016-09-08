import os
import logging
from nslocapysation import constants
from nslocapysation.utils.is_m_implementation_file import is_implementation_file
from nslocapysation.utils.is_lproj_localization_directory import is_lproj_localization_directory


def collect_implementation_file_and_lproj_dir_paths(project_source_root_path):
    """
    Walks the given project_source_root_path and returns a dictionary containing:
        {'m_file_paths': [a list of paths to .m-implementation-files],
         'lproj_file_paths': [a list of paths to .lproj-localization-files]

    :param project_source_root_path: The source root-path of your Xcode project that should be crawled.
    :returns: A dictionary containing lists of file-paths as values.

    :type: str
    :rtype: dict[str, list[str]]
    """
    logging.info('Searching {project_source_root_path} for .m/.swift '
                 'implementation-files and .lproj-localization-directories.'
                 ''.format(project_source_root_path=project_source_root_path))

    result = {constants.IMPLEMENTATION_FILE_PATHS_KEY: [],
              constants.LPROJ_DIR_PATHS_KEY: []}

    num_of_implementation_files = 0
    num_of_lproj_localization_directories = 0

    for dir_path, subdir_names, files in os.walk(project_source_root_path):

        if is_lproj_localization_directory(dir_path):
            result[constants.LPROJ_DIR_PATHS_KEY].append(dir_path)
            num_of_lproj_localization_directories += 1
            logging.debug('Found localization-directory at path "{dir_path}"'
                          ''.format(dir_path=dir_path))
        for file_ in files:
            if is_implementation_file(file_):
                d_path = os.path.join(dir_path, file_)
                result[constants.IMPLEMENTATION_FILE_PATHS_KEY].append(d_path)
                num_of_implementation_files += 1
                logging.debug('Found implementation-file "{file_}" at path "{dir_path}"'
                              ''.format(file_=file_,
                                        dir_path=dir_path))

    logging.info('Found {num} implementation-files.'
                 ''.format(num=num_of_implementation_files))
    logging.info('Found {num} localization-directories.'
                 ''.format(num=num_of_lproj_localization_directories))
    return result
