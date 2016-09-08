__author__ = 'Jan Nash'
__version__ = "0.2"
__license__ = "MIT"

VERSION = "%s v" + __version__


def parse_args():
    """
    Parses command-line arguments and returns the parsed namespace-object.
    """
    import argparse
    import os

    parser = argparse.ArgumentParser(version=VERSION)

    parser.add_argument(
        '-p', '--path',
        action='store', default=os.getcwd(), dest='project_source_root_path',
        help='The path to the Xcode-project\'s source-root folder that will be walked. '
             'Defaults to the current working directory.')

    parser.add_argument(
        '-u', '--update',
        action='store_true', dest='update',
        help='If set, the keys of missing translations will be written to the strings-files.')

    parser.add_argument(
        '-d', '--debug',
        action='store_true', default=False, dest='debug',
        help='Set logging level to DEBUG. Beware, it\'s gonna be verbose :).')

    parser.add_argument(
        '-c', '--custom-macros',
        action='store', nargs='*', dest='custom_macros',
        help='Custom macros that are used in the project. For help regarding the format of those custom macros '
             'see documentation of nslocapysation.classes.localized_string.LocalizedString')

    parser.add_argument(
        '-i', '--ignore',
        action='store', nargs='*', dest='ignore_language_codes', default=(),
        help='Language codes for which missing translations should be disregarded.'
             'This is useful if you are lazy and use the UI-string of that language as key.')

    return parser.parse_args()


def main(cmd_args):
    import logging
    from nslocapysation import constants
    from nslocapysation.tools.collect_m_file_and_lproj_dir_paths import collect_implementation_file_and_lproj_dir_paths
    from nslocapysation.tools.collect_localized_strings import collect_localized_strings
    from nslocapysation.tools.collect_localizable_strings_files import collect_localizable_strings_files
    from nslocapysation.tools.check_translations import check_translations
    from nslocapysation.classes.ns_localized_string_macro import NSLocalizedStringMacro

    if cmd_args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    file_path_dict = collect_implementation_file_and_lproj_dir_paths(cmd_args.project_source_root_path)

    implementation_file_paths = file_path_dict[constants.IMPLEMENTATION_FILE_PATHS_KEY]

    localization_file_paths = file_path_dict[constants.LPROJ_DIR_PATHS_KEY]

    custom_macros = [NSLocalizedStringMacro(format_=fmt) for fmt in cmd_args.custom_macros]

    localized_strings = collect_localized_strings(implementation_file_paths=implementation_file_paths,
                                                  custom_macros=custom_macros)

    localizable_strings_files = collect_localizable_strings_files(localization_dir_paths=localization_file_paths)

    check_translations(translation_files=localizable_strings_files,
                       localized_strings=localized_strings,
                       update=cmd_args.update,
                       ignore_language_codes=cmd_args.ignore_language_codes)

if __name__ == '__main__':
    cl_args = parse_args()
    main(cl_args)
