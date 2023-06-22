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

import os
import sys

from typing import Optional
from translate import Translator
from colorscript import ColorScript


class IO(object):
    """ Subclass of badges module.

    This subclass of badges module is intended for
    providing an implementation of I/O.
    """

    def __init__(self, lang: Optional[str] = None,
                 dictionary: Optional[str] = None,
                 log: Optional[str] = None) -> None:
        """ Initialize I/O.

        :param Optional[str] lang: language to translate to
        :param Optional[str] dictionary: path to save translated messages
        :param Optional[str] log: log to file
        :return None: None
        """

        super().__init__()

        if lang:
            self.translator = Translator(to_lang=lang)
        else:
            self.translator = None

        self.dictionary = dictionary
        self.log = log

        self.color_script = ColorScript()

    def print(self, message: str = '', start: str = '%remove',
              end: str = '%newline', translate: bool = True) -> None:
        """ Print string.

        :param str message: message to print
        :param str start: string to print before the message
        :param str end: string to print after the message
        :param bool translate: True to translate else False
        :return None: None
        """

        if self.translator and translate:
            found = False

            if self.dictionary and os.path.exists(self.dictionary):
                with open(self.dictionary, 'r') as f:
                    messages = f.readlines()
                    message_dict = {entry.split(':')[0]: entry.split(':')[1].strip() for entry in messages}

                    if message in message_dict:
                        message = message_dict[message]
                        found = True

            if not found:
                old_message = message
                full_message = []

                for word in message.split():
                    if not any(command in word for command in self.color_script.commands):
                        try:
                            full_message.append(self.translator.translate(word))
                            continue

                        except Exception:
                            pass

                    full_message.append(word)

                message = ' '.join(full_message)

                if self.dictionary:
                    with open(self.dictionary, 'a') as f:
                        f.write(f'{old_message}:{message}\n')
                        f.flush()

        line = self.color_script.parse(start + message + end)

        sys.stdout.write(line)
        sys.stdout.flush()

        if self.log:
            with open(self.log, 'a') as f:
                f.write(line)
                f.flush()
