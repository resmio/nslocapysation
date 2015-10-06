__author__ = 'JanNash'

import logging
import os
import re
from nslocapysation.classes.dynamic_localized_string import DynamicLocalizedString
from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.ns_localized_string_macro import NSLocalizedStringMacro
from nslocapysation.utils.is_literal_NSString import is_literal_NSString


DEFAULT_MACRO = NSLocalizedStringMacro(format_='NSLocalizedString(@"key", @"comment")')

def collect_localized_strings(implementation_file_paths, custom_macros=()):
    """
    Collects all occurrences of the DEFAULT_MACRO and the given custom_macros
    in the given implementation_file_paths and returns the set of LocalizedString instances.

    :param implementation_file_paths: The paths to the .m-implementation-files that should be searched.
    :param custom_macros: Optional custom macros that are used in the project.
                          See NSLocalizedStringMacro for further information.
    :returns: A set of LocalizedString instances representing all different localizable strings that are used
              throughout the project. For the specs of how they are different, see LocalizedString.__hash__()
              and LocalizedString.__eq__().

    :type implementation_file_paths: list[str]
    :type custom_macros: list[NSLocalizedStringMacro]
    :rtype: set
    """
    result = set()

    macros = [DEFAULT_MACRO] + list(custom_macros)

    logging.info('Searching for the following macros: {macros}'
                 ''.format(macros=", ".join(str(macro) for macro in macros)))

    occurrence_counts = {macro: 0 for macro in macros}

    for file_path in implementation_file_paths:

        with open(file_path, mode='r') as implementation_file:
            lines = implementation_file.readlines()

        file_ = os.path.basename(file_path)
        logging.debug('Reading file {file_}.'
                      ''.format(file_=file_))

        for line_index, line in enumerate(lines):
            line_number = line_index + 1

            logging.debug('Reading line {line}'
                          ''.format(line=line.strip('\n')))

            for macro in macros:
                logging.debug('Searching for occurrences of macro {macro_format}'
                              ''.format(macro_format=macro.format_))

                matches = re.findall(macro.getRegex(), line)

                if not matches:
                    logging.debug('No matches for macro {macro} in line {line_number}'
                                  ''.format(macro=macro,
                                            line_number=line_number))
                    continue
                else:
                    num_of_matches = len(matches)
                    logging.debug('Found {num_of_matches} occurrence of macro {macro} in line {line_number}'
                                  ''.format(num_of_matches=num_of_matches,
                                            macro=macro,
                                            line_number=line_number))
                    occurrence_counts[macro] += len(matches)

                for occurrence_index, match in enumerate(matches):
                    if macro.has_comment:
                        key, comment = match
                    else:
                        key = match
                        comment = None

                    if not is_literal_NSString(key):
                        logging.warning('Attention, there seems to be a dynamic usage of {macro} in file {file_}, '
                                        'line {line_number}, occurrence {occurrence_index}!\n'
                                        'Please check that every possible value of the supplied variable '
                                        '"{variable}" has sufficient localizations!'
                                        ''.format(macro=macro,
                                                  file_=file_,
                                                  line_number=line_number,
                                                  occurrence_index=occurrence_index,
                                                  variable=key))

                        localizedString = DynamicLocalizedString(macro=macro,
                                                                 key=key,
                                                                 comment=comment,
                                                                 full_sourcefile_path=file_path,
                                                                 sourcefile_line_number=line_number,
                                                                 line_occurrence_index=occurrence_index)
                    else:
                        localizedString = LocalizedString(macro=macro,
                                                          key=key,
                                                          comment=comment,
                                                          full_sourcefile_path=file_path,
                                                          sourcefile_line_number=line_number,
                                                          line_occurrence_index=occurrence_index)

                    result.add(localizedString)

    for macro in macros:
        logging.info('Found {num} occurrences of macro {macro} in total'
                      ''.format(num=occurrence_counts[macro],
                                macro=macro))

    logging.info('Found {num} distinct localizable strings in total.'
                 ''.format(num=len(result)))

    return result
