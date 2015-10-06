__author__ = 'JanNash'

import logging
import os
import re

from classes.localized_string import LocalizedString
from nslocapysation.classes.ns_localized_string_macro import NSLocalizedStringMacro

DEFAULT_MACRO = NSLocalizedStringMacro(format_='NSLocalizedString(@"key", @"comment")')

def collect_macro_occurrences(project_source_root_path, custom_macros=()):
    result = set()

    macros = [DEFAULT_MACRO] + list(custom_macros)

    logging.debug('Searching "{project_source_root_path}" for the following macros: {macros}'
                          ''.format(project_source_root_path=project_source_root_path,
                                    macros=", ".join(str(macro) for macro in macros)))



    def is_literal_NSString(string):
        return string[0:2] == '@"'

    number_of_scanned_implementation_files = 0

    occurrence_counts = {macro: 0 for macro in macros}

    for dir_path, subdir_names, files in os.walk(project_source_root_path):
        for file_ in files:
            if not is_implementation_file(file_):
                logging.debug('Skipping file {file}.'
                              ''.format(file=file_))
                continue

            number_of_scanned_implementation_files += 1

            file_path = os.path.join(dir_path, file_)
            with open(file_path, mode='r') as implementation_file:
                lines = implementation_file.readlines()

            logging.debug('Reading file {file_}.'
                          ''.format(file_=file_))

            for line_number in range(len(lines)):

                line = lines[line_number]

                for macro in macros:
                    matches = re.findall(macro.getRegex(), line)

                    if matches:
                        occurrence_counts[macro] += len(matches)

                    for occurrence_index, match in enumerate(matches):
                        if macro.has_comment:
                            key, comment = match
                        else:
                            key = match
                            comment = None

                        if not is_literal_NSString(key):
                            logging.warning('Attention, there seems to be a dynamic usage of {macro} in file {file}, '
                                            'line {line_number}, occurrence {occurrence_index}!\n'
                                            'Please check that every possible value of the supplied variable '
                                            '"{variable}" has sufficient localizations!'
                                            ''.format(macro=macro,
                                                      file=file_,
                                                      line_number=line_number,
                                                      occurrence_index=occurrence_index,
                                                      variable=key))
                        else:
                            localizedString = LocalizedString(macro=macro,
                                                              key=key,
                                                              comment=comment,
                                                              full_sourcefile_path=file_path,
                                                              sourcefile_line_number=line_number,
                                                              line_occurrence_index=occurrence_index)
                            result.add(localizedString)

    logging.info('Scanned {num} implementation-files.'
                  ''.format(num=number_of_scanned_implementation_files))
    for macro in macros:
        logging.info('Found {num} occurrences of macro {macro}'
                      ''.format(num=occurrence_counts[macro],
                                macro=macro))

    logging.info('Found {num} distinct localizable strings.'
                 ''.format(num=len(result)))

    return result


logging.basicConfig(level=logging.INFO)

a = collect_macro_occurrences(
        project_source_root_path='/Users/JanNash/Desktop/resmio/repos/resmio-tables/ResmioApp',
        custom_macros=[NSLocalizedStringMacro(format_='NSL(@"key")')]
    )
