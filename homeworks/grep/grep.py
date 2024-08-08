
import argparse
import sys
import re

def output(line):
    print(line)

def prepare_output(line, line_number=None, delimiter=':'):
    if line_number is not None:
        output(f"{line_number}{delimiter}{line}")
    else:
        output(line)

def grep(lines, params):
    counter = line_number = 0
    context = {}
    context_found = []

    use_context = params.context or params.before_context or params.after_context

    for line in lines:
        line_number += 1
        line = origin_line = line.rstrip()
        pattern = params.pattern

        if use_context:
            context[line_number] = origin_line

        if params.ignore_case:
            pattern = pattern.lower()
            line = line.lower()

        pattern = pattern.replace('?', '.').replace('*', '.*')
        result = re.search(pattern, line)

        if (params.invert and not result) or (not params.invert and result):
            if params.count:
                counter += 1
            elif use_context:
                context_found.append(line_number)
            else:
                prepare_output(origin_line, str(line_number) if params.line_number else None)


    if params.count:
        prepare_output(str(counter))
    
    result_lines = []
    if params.context:
        result_lines = [ln + offset for ln in context_found for offset in range(-params.context, params.context + 1)]
        
        # Первый вариант этого кода:
        # result_lines = set()
        # for ln in context_found:
        #     for offset in range(params.context * 2 + 1):
        #         result_lines.add(ln - (offset - params.context))

    if params.before_context:
        result_lines = [ln + offset for ln in context_found for offset in range(-params.before_context, 1)]

    if params.after_context:
        result_lines += [ln + offset for ln in context_found for offset in range(params.after_context + 1)]

    if result_lines:
        result_lines = set(result_lines)
        for line in result_lines:
            if line not in context:
                continue
            if params.line_number:
                prepare_output(context[line], str(line), ':' if line in context_found else '-')
            else:
                output(context[line])


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v', action="store_true", dest="invert", default=False, help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i', action="store_true", dest="ignore_case", default=False, help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin.readlines(), params)


if __name__ == '__main__':
    main()
