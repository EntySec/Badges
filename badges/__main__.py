"""
MIT License

Copyright (c) 2020-2023 EntySec

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

from .io import IO


class Badges(object):
    """ Main class of badges module.

    This main class of badges module is intended for
    providing various printing interfaces.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()

        self.io = IO(*args, **kwargs)

    def print_empty(self, *args, **kwargs) -> None:
        """ Print string with empty start.

        :return None: None
        """

        self.io.print(*args, **kwargs)

    def print_usage(self, message: str, start: str = '%remove', *args, **kwargs) -> None:
        """ Print string with Usage: start.

        :param str message: message to print
        :param str start: string to print before the message
        :return None: None
        """

        self.print_empty(message, f"{start}Usage: ", *args, **kwargs)

    def print_process(self, message: str, start: str = '%remove', *args, **kwargs) -> None:
        """ Print string with [*] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return None: None
        """

        self.print_empty(message, f"{start}%bold%blue[*]%end ", *args, **kwargs)

    def print_success(self, message: str, start: str = '%remove', *args, **kwargs) -> None:
        """ Print string with [+] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return None: None
        """

        self.print_empty(message, f"{start}%bold%green[+]%end ", *args, **kwargs)

    def print_error(self, message: str, start: str = '%remove', *args, **kwargs) -> None:
        """ Print string with [-] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return None: None
        """

        self.print_empty(message, f"{start}%bold%red[-]%end ", *args, **kwargs)

    def print_warning(self, message: str, start: str = '%remove', *args, **kwargs) -> None:
        """ Print string with [!] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return None: None
        """

        self.print_empty(message, f"{start}%bold%yellow[!]%end ", *args, **kwargs)

    def print_information(self, message: str, start: str = '%remove', *args, **kwargs) -> None:
        """ Print string with [i] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return None: None
        """

        self.print_empty(message, f"{start}%bold%white[i]%end ", *args, **kwargs)

    def input_empty(self, *args, **kwargs) -> list:
        """ Input string with empty start.

        :return str: string
        """

        return self.io.input(*args, **kwargs)

    def input_question(self, message: str, start: str = '%remove%end', *args, **kwargs) -> list:
        """ Input string with [?] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return str: string
        """

        return self.input_empty(message, f"{start}%bold%white[?]%end ", *args, **kwargs)

    def input_arrow(self, message: str, start: str = '%remove%end', *args, **kwargs) -> list:
        """ Input string with [>] start.

        :param str message: message to print
        :param str start: string to print before the message
        :return str: string
        """

        return self.input_empty(message, f"{start}%bold%white[>]%end ", *args, **kwargs)
