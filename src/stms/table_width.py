#!/usr/bin/env python


def get_width_percentage(widths):
    percentages = []
    total_width = sum(widths)
    for width in widths:
        percentage = int(width/total_width * 100)
        percentages.append(percentage)
    total_width = sum(percentages)
    diff = 100 - total_width
    percentages[-1] += diff
    return percentages


def parse(inputfile, outputfile):
    tables = []
    with open(inputfile, 'r') as inputf:
        with open(outputfile, 'w') as outputf:
            for line in inputf:
                lines = []
                if line.startswith('##'):
                    while not line.startswith('##'):
                        lines.append(line)
                        line = inputf.readline()
                    widths = get_width_percentage(lines)
                    tables.append(widths)
    return tables


if __name__ == '__main__':
    print(get_width_percentage([860, 3770, 2800, 990]))
