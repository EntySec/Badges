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
import io
import sys
import getch

from datetime import datetime
from colorscript import ColorScript

from typing import Callable, Any, Optional
from contextlib import redirect_stdout, redirect_stderr

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import ANSI


class IO(object):
    """ Subclass of badges module.

    This subclass of badges module is intended for
    providing an implementation of I/O.
    """

    @staticmethod
    def set_log(log: str) -> None:
        """ Set log path.

        :param str log: log path
        :return None: None
        """

        globals()['log'] = log

    @staticmethod
    def set_history(history: str) -> None:
        """ Set history path.

        :param str history: history path
        :return None: None
        """

        globals()['history'] = history

    @staticmethod
    def set_less(less: bool) -> None:
        """ Enable/disable less-like output.

        :param bool less: True to enable, False to disable
        :return None: None
        """

        globals()['less'] = less

    def print_function(self, target: Callable[..., Any], *args, **kwargs) -> Any:
        """ Execute function and print its stdout.

        :param Callable[..., Any] target: function
        :return Any: function return value
        """

        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            result = target(*args, **kwargs)
            output = buf.getvalue()

        self.print_less(output)
        return result

    @staticmethod
    def print_less(data: str) -> None:
        """ Print data in less format.

        :param str data: data to print
        :return None: None
        """

        try:
            columns, rows = os.get_terminal_size()

        except Exception:
            sys.stdout.write(data)
            sys.stdout.flush()

            return

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

            sys.stdout.write(ColorScript().parse('%remove'))
            sys.stdout.flush()

            if user_input == 'q':
                return

            start_index = end_index + 1
            end_index = start_index

    @staticmethod
    def input(message: str = '', start: str = '%end', end: str = '', *args, **kwargs) -> None:
        """ Input string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :return None: None
        """

        if 'prompt_session' not in globals():
            history = globals().get('history', None)

            if history:
                globals()['prompt_session'] = PromptSession(
                    history=FileHistory(history))
            else:
                globals()['prompt_session'] = PromptSession()

        session = globals()['prompt_session']
        line = ColorScript().parse(str(start) + str(message) + str(end))
        use_log = globals().get("log")

        data = session.prompt(ANSI(line), *args, **kwargs)

        if use_log:
            with open(use_log, 'a') as f:
                f.write(line + data + '\n')
                f.flush()

        return data

    def print(self, message: str = '', start: str = '%remove%end', end: str = '%newline',
              time: bool = False, log: Optional[bool] = None,
              less: Optional[bool] = None) -> None:
        """ Print string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :param bool time: show timestamp after start
        :param Optional[bool] log: override global log
        :param Optional[bool] less: override global less
        :return None: None
        """

        if time:
            start = str(start) + datetime.now().strftime('%H:%M:%S - ')

        line = ColorScript().parse(str(start) + str(message) + str(end))

        use_log = log if log is not None else globals().get("log")
        use_less = less if less is not None else globals().get("less", True)

        if use_less:
            self.print_less(line)
        else:
            sys.stdout.write(line)
            sys.stdout.flush()

        if use_log:
            with open(use_log, 'a') as f:
                f.write(line)
                f.flush()
