#!/opt/clintosaurous/venv/bin/python3 -Bu

""" Various text string operations. """

# Version: 1.0.0
# Last Updated: 2022-05-30
#
# Change Log:
#   v1.0.0:
#       Initial creation. (2022-05-30)
#
# Note: See repository commit logs for change details.


# Required modules.
import re


def center(text="", width=78, wrap=True):

    """
    Takes the string passed and centers it with the width. Width is optional
    and defaults to 78 to fit in an 80 character terminal. For strings
    longer than width, if wrap is true, the lines are wrapped with each line
    in the wrap centered to width. wrap default is true. Trailing spaces are
    not returned.

        >>> import clintosaurous.text.text
        >>> clintosaurous.text.text.center("Test center.")
        '                                 Test center.'
    """

    if not isinstance(text, str):
        text = str(text)
    text_len = len(text)
    if not text_len:
        return

    return_text = ""

    # if not line wrapping, just use line text
    if not wrap:
        for line in text.split("\n"):
            line = line.strip()
            line_len = len(line)
            start_point = int(width / 2 - line_len / 2)
            return_text = "{0}{1}{2}\n".format(
                return_text, " "*start_point, line
            )

        return return_text.rstrip()

    # start line wrapping logic
    text = text.replace("\n", " ")

    lines = []
    if text_len > width:
        line = ""
        line_len = 0
        for word in text.split(" "):
            word_len = len(word)
            line_len = len(line)

            if not word_len:
                if line_len + 1 > width:
                    line = re.sub(r'\s+$', '', line)
                    lines.append(line)
                    line = ""
                else:
                    line = line + " "

            elif word_len > width:
                if line_len:
                    line = re.sub(r'\s+$', '', line)
                    lines.append(line)
                    line = ""

                for _char in re.split("", word):
                    line = line + _char
                    if len(line) >= width:
                        lines.append(line)
                        line = ""

            elif word_len + line_len + 1 > width:
                line = re.sub(r'\s+$', '', line)
                lines.append(line)
                line = word

            else:
                line = line + " " + word

        if len(line):
            line = re.sub(r'\s+$', '', line)
            lines.append(line)

    else:
        lines.append(text)

    for line in lines:
        line_len = len(line)
        start_position = int(width / 2 - line_len / 2)

        if start_position > 0:
            return_text = return_text.ljust(start_position - 1)

        return_text = return_text + line + "\n"

    return return_text.rstrip()

# End center()


def expand_range(ranges_str=None):

    """
    Takes integer ranges and expands them to all numbers in the range. Format
    is a dash between ranges and a comma to separate ranges.

        >>> import clintosaurous.text
        >>> clintosaurous.text.expand_range("1-3,5-6,8,10-12")
        [1, 2, 3, 5, 6, 8, 10, 11, 12]
    """

    if ranges_str and isinstance(ranges_str, int):
        return ranges_str
    elif not len(ranges_str):
        return

    ranges = []
    for range_str in ranges_str.split(","):
        if not len(range_str):
            continue

        if isinstance(range_str, int):
            ranges.append(range_str)

        else:
            range_nums = range_str.split("-")

            if len(range_nums) < 2:
                ranges.append(int(range_nums[0]))

            else:
                start_num = int(range_nums[0])
                end_num = int(range_nums[1])
                if start_num > end_num:
                    tmp_num = start_num
                    start_num = end_num
                    end_num = tmp_num

                for number in range(start_num, end_num + 1):
                    ranges.append(number)

    return sorted(ranges)

# End expand_range()


def number_commas(number):

    """
    Adds commas to long numbers.

        >>> import clintosaurous.text
        >>> clintosaurous.text.number_commas(1000000)
        '1,000,000'
    """

    if isinstance(number, str):
        if re.match(r'^-?\d+$', number):
            number = int(number)
        elif re.match(r'^-?\d+\.\d+$', number):
            number = float(number)
        else:
            return number
    elif not isinstance(number, int) and not isinstance(number, float):
        return number

    return "{:,}".format(number)

# End number_commas()


def pluralize(word, number):

    """
    Takes the word supplied and the number of items and converts the word to a
    plural format. It accounds for not making one number plural, words ending
    in y and all uppercase words.

        >>> import clintosaurous.text
        >>> clintosaurous.text.pluralize("test", 1)
        'test'
        >>> clintosaurous.text.pluralize("test", 2)
        'tests'
        >>> clintosaurous.text.pluralize("testy", 1)
        'testy'
        >>> clintosaurous.text.pluralize("testy", 2)
        'testies'
        >>> clintosaurous.text.pluralize("TEST", 1)
        'TEST'
        >>> text.pluralize("TEST", 2)
        'TESTS'
    """

    if isinstance(word, int) or isinstance(word, float):
        word = str(word)

    if not isinstance(word, str):
        return word
    elif not isinstance(number, int):
        return word
    elif number == 1:
        return word

    if word.isupper():
        uppercase = 1
    else:
        uppercase = 0

    if len(word) <= 1:
        return_txt = word + "s"

    else:
        split_str = [char for char in word]
        base = "".join(split_str[0:-1])
        last_char = split_str[-1]

        if last_char.lower() == "y":
            if re.match(r'[aeiou]', split_str[-2]):
                return_txt = word + "s"
            else:
                return_txt = base + "ies"

        elif last_char.lower() == "s":
            if split_str[-2].lower() == 'e':
                return_txt = word
            else:
                return_txt = word + "es"

        else:
            return_txt = word + "s"

    if uppercase:
        return return_txt.upper()
    else:
        return return_txt

# End pluralize()


def table(rows=None, title=None, headings=True):

    """
    Creates a text based table with the given title and rows.
    Title and headings are optional.

    rows
        Rows of data.
    title
        Optional title to add to the top of the table.
    headings
        Boolean if the first row are table headings.
    """

    # Set headings row.
    if headings:
        headings = rows[0]
        del rows[0]

    # number of columns in table
    col_count = 1
    # max width of all columns
    col_widths = []

    # if headings, get heading column count and set column widths
    if headings:
        col_count = len(headings)

        # loop through headings and set width
        for i in range(len(headings)):
            if not isinstance(headings[i], str):
                headings[i] = str(headings[i])

            col_width = len(headings[i])

            # if no width, set to 1
            if col_width:
                col_widths.append(col_width)
            else:
                col_widths.append(1)

    # loop through rows to get column count, widths
    for row in rows:
        row_len = len(row)

        # increase column count if more row columns than previously seen
        if row_len > col_count:
            col_count = row_len

        # loop through row checking width and data type
        for i in range(len(row)):
            if not isinstance(row[i], str):
                row[i] = str(row[i])

            col_width = len(row[i])

            if len(col_widths) <= i:
                if col_width:
                    col_widths.append(col_width)
                else:
                    col_widths.append(1)
            else:
                if col_width > col_widths[i]:
                    col_widths[i] = col_width

    # return box text
    table_txt = ""

    # if table title, print title header
    if title:
        if not isinstance(title, str):
            title = str(title)

        # determine top bar width
        dash_width = len(col_widths) * 3 - 1
        for width in col_widths:
            dash_width = dash_width + width

        text_width = dash_width - 2

        table_txt = table_txt + "+" + "-"*dash_width + "+\n"
        centeredtitle = center(title, text_width)
        for line in centeredtitle.split("\n"):
            table_txt = "{0}| {1}{2} |\n".format(
                table_txt, line, " "*(text_width - len(line))
            )

    break_line = ""
    for i in range(len(col_widths)):
        break_line = "{0}+-{1}-".format(break_line, "-"*col_widths[i])
    break_line = "{0}+\n".format(break_line)

    # add headings
    if headings:
        table_txt = table_txt + break_line

        # loop through headings and add to row
        for i in range(col_count):
            try:
                heading = headings[i]
            except IndexError:
                heading = ""

            table_txt = "{0}| {1}{2} ".format(
                table_txt, heading, " "*(col_widths[i] - len(heading))
            )

        table_txt = table_txt + "|\n"

    table_txt = table_txt + break_line

    # loop through data rows
    for row in rows:

        # loop through headings and add to row
        for i in range(col_count):
            try:
                value = row[i]
            except IndexError:
                value = ""

            table_txt = "{0}| {1}{2} ".format(
                table_txt, value, " "*(col_widths[i] - len(value))
            )

        table_txt = table_txt + "|\n"

    table_txt = table_txt + break_line

    return table_txt

# End table()
