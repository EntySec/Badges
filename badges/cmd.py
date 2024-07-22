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
import importlib

from badges import Tables, Badges
from colorscript import ColorScript

from typing import (
    Any,
    Optional,
    Tuple,
    Union
)

from pex.string import String

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import ANSI


class Command(Tables, Badges):
    """ Subclass of badges module.

    This subclass of badges module is a representation of
    external command object.
    """

    def __init__(self, info: dict = {}) -> None:
        """ Initialize command

        :param dict info: command details
        :return None: None
        """

        self.info = {
            'Category': "",
            'Name': "",
            'Authors': [
                ''
            ],
            'Description': "",
            'Usage': "",
            'MinArgs': 0
        }
        self.info.update(info)

        self.complete = {}

    def run(self, args: list) -> None:
        """ Run this command.

        :param list args: arguments
        :return None: None
        """

        pass


class Cmd(Tables, Badges):
    """ Subclass of badges module.

    This subclass of badges module is intended to provide
    a wrapper for CLIs. Based on cmd.Cmd python module.
    """

    def __init__(self,
                 prompt: str = '%red$ %end',
                 intro: Optional[str] = '',
                 path: Optional[list] = [],
                 history: Optional[str] = None,
                 **kwargs) -> None:
        """ Initialize cmd.

        :param str prompt: prompt to apply
        :param Optional[str] intro: message to print before loop
        :param Optional[list] path: list of directories to load
        commands from
        :param Optional[str] history: history file path
        :return None: None
        """

        self.intro = ColorScript().parse(intro)
        self.prompt = ColorScript().parse(prompt)

        self.internal = []
        self.external = {}
        self.complete = {}

        for name in dir(self.__class__):
            if name.startswith('do_'):
                self.internal.append(name[3:])
                self.complete[name[3:]] = None

        for commands in path:
            self.load_external(commands, **kwargs)

        self.completer = NestedCompleter.from_nested_dict(self.complete)

        if history:
            self.session = PromptSession(
                history=FileHistory(history),
                complete_while_typing=True,
                auto_suggest=AutoSuggestFromHistory()
            )
        else:
            self.session = PromptSession(
                complete_while_typing=True,
                auto_suggest=AutoSuggestFromHistory()
            )

    def delete_external(self, name: str) -> None:
        """ Delete external command.

        :param str name: command name
        :return None: None
        """

        self.external.pop(name, None)
        self.complete.pop(name, None)

    def add_external(self, external: dict) -> None:
        """ Add external commands.

        :param dict external: dictionary containing commands
        and their informations (e.g. all info + Method and Complete)
        :return None: None
        """

        for name, info in external.items():
            if 'Method' not in info:
                continue

            self.external[name] = info
            self.complete[name] = {}

            if 'Complete' in info:
                self.complete[name].update(info['Complete'])

            if 'Options' in info:
                self.complete[name].update(
                    {k: None if v[0] == '' else {o: None for o in v[0].split()}
                     for k, v in info['Options'].items()})

    def load_external(self, path: Optional[str] = None, **kwargs) -> None:
        """ Load/reload external commands.

        :param Optional[str] path: path to load from
        :return None: None
        """

        for file in os.listdir(path):
            if not file.endswith('py'):
                continue

            try:
                commands = path + '/' + file
                spec = importlib.util.spec_from_file_location(commands, commands)
                object = importlib.util.module_from_spec(spec)

                spec.loader.exec_module(object)
                object = object.ExternalCommand()

                for attr, sub in kwargs.items():
                    setattr(object, attr, sub)

                name = object.info['Name']

                self.external[name] = {'Method': object.run}
                self.external[name].update(object.info)

                self.complete[name] = object.complete
                if 'Options' in object.info:
                    self.complete[name].update(
                        {k: None if v[0] == '' else {o: None for o in v[0].split()}
                         for k, v in object.info['Options'].items()})

            except Exception as e:
                self.print_error(f"Failed to load {file[:-3]} command!")
                self.print_error(str(e))

            self.completer = NestedCompleter.from_nested_dict(self.complete)

    def do_help(self, _) -> None:
        """ Show all available commands.

        :return None: None
        """

        data = {}
        headers = ('Command', 'Description')

        for command in sorted(self.internal):
            if 'core' not in data:
                data['core'] = []

            description = getattr(self, 'do_' + command).__doc__.strip().split('\n')[0]

            data['core'].append((
                command, description))

        for command in sorted(self.external):
            category = self.external[command]['Category']
            description = self.external[command]['Description']

            if category not in data:
                data[category] = []

            data[category].append((command, description))

        for category in sorted(data):
            self.print_table(f"{category} Commands", headers, *data[category])

    def parse_usage(self, info: dict) -> None:
        """ Print usage for specific command info.

        :param dict info: dictionary of command info
        :return None: None
        """

        self.print_usage(info['Usage'])

        if 'Options' not in info:
            return

        headers = ('Option', 'Arguments', 'Description')
        data = []

        for option in info['Options']:
            details = info['Options'][option]
            data.append((option, details[0], details[1]))

        self.print_table('Options', headers, *data)

    def verify_command(self, args: list) -> Tuple[bool, Union[str, list, None]]:
        """ Check if command or shortcut exists.

        :param list args: list of args
        :return Tuple[bool, Union[str, list, None]]: None if not found or tuple of status and if command is single,
            object, otherwise list of similar commands.
        """

        commands = {}

        for name, object in self.external.items():
            for i in range(len(name) + 1):
                prefix = name[:i]

                if prefix not in commands:
                    commands[prefix] = name

                elif commands[prefix] != name:
                    commands[prefix] = None

        if args[0] not in commands:
            return False, None

        result = commands[args[0]]

        if result:
            return True, result

        else:
            conflict = [name for name, object in self.external.items() if name.startswith(args[0])]

            if args[0] in conflict:
                return True, args[0]

            return False, conflict

    @staticmethod
    def verify_args(args: list, info: dict) -> bool:
        """ Check if arguments correct for command.

        :param list args: list of args
        :param dict info: dictionary of command info
        :return bool: status, True if correct else False
        """

        if len(args) - 1 < info['MinArgs']:
            return False

        if 'Options' in info:
            if len(args) > 1:
                if args[1] in info['Options']:
                    if len(args) - 2 < len(
                            info['Options'][args[1]][0].split()
                    ):
                        return False
                else:
                    return False

        return True

    def loop(self) -> None:
        """ Run main loop.

        :return None: None
        """

        self.preloop()

        if self.intro:
            self.print_empty(self.intro)

        while True:
            with patch_stdout(raw=True):
                line = self.session.prompt(
                    ANSI(self.prompt), completer=self.completer)

            if line is None:
                break

            args = String().split_args(line)

            if not args:
                continue

            args = self.precmd(args)
            self.postcmd(self.onecmd(args))

        self.postloop()

    def preloop(self) -> None:
        """ Do something before cmdloop.

        :return None: None
        """

        return

    def postloop(self) -> None:
        """ Do something after cmdloop.

        :return None: None
        """

        return

    def precmd(self, args: list) -> list:
        """ Do something before executing command.

        :param list args: list of args
        :return str: command
        """

        return args

    def postcmd(self, args: list) -> None:
        """ Do something after command execution.

        :param list args: list of args
        :return None: None
        """

        return

    def onecmd(self, args: list) -> Tuple[int, list]:
        """ Execute single command.

        :param list args: list of args
        :return Any: command result
        """

        if args[0] in self.internal:
            getattr(self, 'do_' + args[0])(args)
            return args

        status, name = self.verify_command(args)

        if status:
            fixed = [name, *args[1:]]
            command = self.external[name]

            if not self.verify_args(fixed, command):
                self.parse_usage(command)

            else:
                command['Method'](fixed)

            return fixed

        if name is not None:
            self.print_warning(f"Did you mean? {', '.join(name)}")

        self.default(args)
        return args

    def default(self, args: list) -> Any:
        """ Failure handle.

        :param list args: list of args
        :return Any: command result
        """

        self.print_error(f"Unrecognized command: {args[0]}")
