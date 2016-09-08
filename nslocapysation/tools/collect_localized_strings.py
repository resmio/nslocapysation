import logging
import os
import re
from nslocapysation.classes.dynamic_localized_string import DynamicLocalizedString
from nslocapysation.classes.localized_string import LocalizedString
from nslocapysation.classes.ns_localized_string_macro import NSLocalizedStringMacro
from nslocapysation.utils.is_literal_string import is_literal_string
from nslocapysation.utils.n_ import n_


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
    :rtype: set[LocalizedString]
    """
    result = set()

    macros = [DEFAULT_MACRO] + list(custom_macros)

    logging.info('Searching for macros: {macros}'
                 ''.format(macros=", ".join(str(macro) for macro in macros)))

    occurrence_counts = {macro: 0 for macro in macros}

    for file_path in implementation_file_paths:

        file_result = set()
        occurrences_in_file = {}

        with open(file_path, mode='r') as implementation_file:
            lines = implementation_file.readlines()

        file_ = os.path.basename(file_path)
        logging.debug('Reading file {file_}.'
                      ''.format(file_=file_))

        for macro in macros:
            occurrences_in_file[macro] = 0

        for line_index, line in enumerate(lines):
            line_number = line_index + 1

            for macro in macros:
                matches = re.findall(macro.get_regex(), line)

                if not matches:
                    continue
                else:
                    num_of_matches = len(matches)
                    occurrence_counts[macro] += num_of_matches
                    occurrences_in_file[macro] += num_of_matches

                for occurrence_index, match in enumerate(matches):
                    occurrence_number = occurrence_index + 1

                    if macro.has_comment:
                        key, comment = match
                    else:
                        key = match
                        comment = None

                    if not is_literal_string(key):
                        logging.warning('Attention, there seems to be a dynamic usage of {macro} in file {file_}, '
                                        'line {line_number}, occurrence number {occurrence_number}! \n'
                                        'Please be sure to check manually that every possible value of the '
                                        'supplied variable "{variable}" has sufficient localizations!'
                                        ''.format(macro=macro,
                                                  file_=file_,
                                                  line_number=line_number,
                                                  occurrence_number=occurrence_number,
                                                  variable=key))

                        localized_string = DynamicLocalizedString(macro=macro,
                                                                  strng=key,
                                                                  comment=comment,
                                                                  full_sourcefile_path=file_path,
                                                                  sourcefile_line_number=line_number,
                                                                  line_occurrence_number=occurrence_number)
                    else:
                        localized_string = LocalizedString(macro=macro,
                                                           strng=key,
                                                           comment=comment,
                                                           full_sourcefile_path=file_path,
                                                           sourcefile_line_number=line_number,
                                                           line_occurrence_number=occurrence_number)

                    file_result.add(localized_string)

        for macro in macros:
            num_of_occurrences_in_file = occurrences_in_file[macro]
            if num_of_occurrences_in_file:
                logging.debug('Found {num} {n_occurrence} of macro {macro} in file {file_}'
                              ''.format(num=num_of_occurrences_in_file,
                                        n_occurrence=n_(num_of_occurrences_in_file, 'occurrence'),
                                        macro=macro,
                                        file_=file_))
        if len(file_result):
            logging.debug('Found keys and comments: (key, comment) {keys_and_comments}'
                          ''.format(keys_and_comments=[(strng.key, strng.comment) for strng in file_result]))

        result = result.union(file_result)

    for macro in macros:
        num = occurrence_counts[macro]
        logging.info('Found {num} {n_occurrence} of macro {macro} in total.'
                     ''.format(num=num,
                               n_occurrence=n_(num, 'occurrence'),
                               macro=macro))

    logging.info('Found {num} distinct localizable {n_string} in total.'
                 ''.format(num=len(result),
                           n_string=n_(len(result), 'string')))

    return result
