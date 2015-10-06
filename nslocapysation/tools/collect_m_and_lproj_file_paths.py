__author__ = 'JanNash'

import os


def collect_m_and_lproj_file_paths(project_source_root_path):
    """
    Walks the given project_source_root_path and returns a dictionary containing:
        {'m_file_paths': [a list of paths to .m-implementation-files],
         'lproj_file_paths': [a list of paths to .lproj-localization-files]

    :param project_source_root_path: The source root-path of your Xcode project that should be crawled.
    :type: str
    :returns: A dictionary containing lists of file-paths as values.
    :rtype: dict[str, list[str]]
    """


    return