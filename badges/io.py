"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
import getch
import readline

from typing import Optional
from colorscript import ColorScript


class IO(object):
    """ Subclass of badges module.

    This subclass of badges module is intended for
    providing an implementation of I/O.
    """

    def __init__(self) -> None:
        """ Initialize I/O.

        :return None: None
        """

        super().__init__()

        self.color_script = ColorScript()

    @staticmethod
    def set_log(log: str) -> None:
        """ Set log path.

        :param str log: log path
        :return None: None
        """

        globals()['log'] = log

    @staticmethod
    def set_less(less: bool) -> None:
        """ Enable/disable less-like output.

        :param bool less: True or False
        :return None: None
        """

        globals()['less'] = less

    def print_less(self, data: str) -> None:
        """ Print data in less format.

        :param str data: data to print
        :return None: None
        """

        columns, rows = os.get_terminal_size()

        lines = data.split('\n')
        num_lines = len(lines)
        start_index = 0
        end_index = rows - 3

        while start_index < num_lines:
            for line in range(start_index, min(end_index + 1, num_lines)):
                if line == num_lines - 1:
                    sys.stdout.write(lines[line])
                    sys.stdout.flush()
                else:
                    sys.stdout.write(lines[line] + '\n')
                    sys.stdout.flush()

            if end_index >= num_lines - 1:
                break

            sys.stdout.write("Press Enter for more, or 'q' to quit:")
            sys.stdout.flush()

            user_input = ''

            while user_input not in ['\n', 'q']:
                user_input = getch.getch()

            sys.stdout.write(self.color_script.parse('%remove'))
            sys.stdout.flush()

            if user_input == 'q':
                return

            start_index = end_index + 1
            end_index = start_index

    def input(self, message: str = '', start: str = '%end%remove', end: str = '') -> None:
        """ Input string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        line = self.color_script.parse_input(str(start) + str(message) + str(end))
        use_log = globals().get("log")

        globals()['prompt'] = line
        data = input(line)

        if use_log:
            with open(use_log, 'a') as f:
                f.write(line + data + '\n')
                f.flush()

        globals().pop('prompt')
        return data

    def print(self, message: str = '', start: str = '%remove', end: str = '%newline') -> None:
        """ Print string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        line = self.color_script.parse(str(start) + str(message) + str(end))

        use_log = globals().get("log")
        use_less = globals().get("less")

        if use_less:
            self.print_less(line)
        else:
            sys.stdout.write(line)
            sys.stdout.flush()

        if use_log:
            with open(use_log, 'a') as f:
                f.write(line)
                f.flush()

        prompt = globals().get("prompt")
        if prompt:
            sys.stdout.write(prompt + readline.get_line_buffer())
            sys.stdout.flush()
