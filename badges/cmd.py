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
import shlex
import traceback
import argparse
import subprocess

import importlib.util

from badges import Tables, Badges
from colorscript import ColorScript

from contextlib import redirect_stdout, redirect_stderr

from typing import (
    Any,
    Optional,
    Tuple,
    Union
)

from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.formatted_text import ANSI


def continue_or_exit() -> None:
    """ Continue loading commands or exit.

    :return None: None
    """

    sys.stdout.write("Press Enter to continue, or 'q' to quit:")
    sys.stdout.flush()

    user_input = ''
    while user_input not in ['\n', 'q']:
        user_input = getch.getch()

    if user_input == 'q':
        sys.exit(0)


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
            'Authors': [],
            'Description': "",
            'Usage': "",
            'MinArgs': 0,
            'Options': [],
            'Method': None,
            'Complete': None,
            'Shorts': {}
        }
        self.info.update(info)

    @staticmethod
    def complete() -> Union[dict, None]:
        """ Provide autocomplete scheme.

        :return dict: nested autocompletion scheme
        """

        return

    def run(self, args: list) -> None:
        """ Run this command.

        :param list args: arguments
        :return None: None
        """

        return


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
                 log: Optional[str] = None,
                 shorts: dict = {},
                 builtins: dict = {},
                 **kwargs) -> None:
        """ Initialize cmd.

        :param str prompt: prompt to apply
        :param Optional[str] intro: message to print before loop
        :param Optional[list] path: list of directories to load
        commands from
        :param Optional[str] history: history file path
        :param Optional[str] log: log file path
        :param dict shorts: dictionary of shortcuts
        :param dict builtins: dictionary of built-ins
        (e.g. ? for help, ! for commands, etc.)
        :return None: None
        """

        self.intro = intro
        self.prompt = prompt

        self.set_intro(intro)
        self.set_prompt(prompt)

        self.internal = []
        self.external = {}
        self.shorts = shorts

        self.complete = {}
        self.dynamic_complete = {}
        self.source = []

        for name in dir(self.__class__):
            if name.startswith('do_'):
                self.internal.append(name[3:])
                self.complete[name[3:]] = None

        for commands in path:
            self.load_external(commands, **kwargs)

        if history:
            self._session = PromptSession(
                history=FileHistory(history),
                complete_while_typing=True,
                auto_suggest=AutoSuggestFromHistory()
            )
        else:
            self._session = PromptSession(
                complete_while_typing=True,
                auto_suggest=AutoSuggestFromHistory()
            )

        self.set_log(log)

        self.builtins = {
            '!': self.system,
            '#': lambda x: x,
            '*': 'help',
            '?': 'help',
            '@': 'clear',
            '.': 'exit',
            ':': 'source',
        }
        self.builtins.update(builtins)

    def system(self, args: list) -> None:
        """ Execute system commands.

        :param list args: arguments
        :return None: None
        """

        if len(args) < 1:
            self.print_usage('!<command>')
            return

        self.print_process(f"Executing system command: {args[0]}%newline")

        try:
            subprocess.run(args)

        except Exception as e:
            self.print_error(f"Failed to execute: {str(e)}!")
            return

    def set_prompt(self, prompt: str) -> None:
        """ Set prompt message.

        :param str prompt: prompt message
        :return None: None
        """

        self.prompt = ColorScript().parse(prompt)

    def set_intro(self, intro: str) -> None:
        """ Set intro message.

        :param str intro: intro message
        :return None: None
        """

        self.intro = ColorScript().parse(intro)

    def delete_external(self, name: str) -> None:
        """ Delete external command.

        :param str name: command name
        :return None: None
        """

        self.external.pop(name, None)
        self.complete.pop(name, None)

    def add_shortcut(self, alias: str, command: str, desc: str = "") -> None:
        """ Add shortcut for command.

        :param str alias: alias name
        (e.g. kill)
        :param str command: command
        (e.g. jobs kill ?1)
        :param str desc: description
        :return None: None
        """

        self.shorts[alias] = [command, desc]

    def add_external(self, external: list) -> None:
        """ Add external commands.

        :param list external: dictionary containing commands
        instances of ExternalCommand
        :return None: None
        """

        for command in external:
            name = command.info['Name']

            if not command.info['Method']:
                continue

            self.external[name] = command.info
            self.complete[name] = {}

            self.shorts.update(command.info['Shorts'])

            if command.info['Complete']:
                self.dynamic_complete[name] = command.info['Complete']

            if not self.complete[name]:
                self.complete[name] = None

    def load_external(self, path: str, **kwargs) -> None:
        """ Load/reload external commands.

        :param str path: path to load from
        :return None: None
        """

        if not os.path.exists(path):
            return

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

                self.external[name] = object.info
                self.external[name].update({'Method': object.run})
                self.complete[name] = {}

                self.shorts.update(object.info['Shorts'])

                if object.complete() is not None:
                    self.dynamic_complete[name] = object.complete

                if not self.complete[name]:
                    self.complete[name] = None

            except Exception:
                self.print_error(f"Failed to load {file[:-3]} command!")
                traceback.print_exc(file=sys.stdout)
                continue_or_exit()

    def do_source(self, args: list) -> None:
        """ Execute specific file as source.

        :param list args: command arguments
        :return None: None
        """

        if len(args) < 2 or not args[1]:
            while True:
                line = self._session.prompt(
                    ANSI(': '),
                    completer=NestedCompleter.from_nested_dict(self.complete))

                if not line:
                    break

                self.source.append(line)

        else:
            self.print_process(f"Executing from file: {args[1]}%newline")
            self.source = open(args[1], 'r').read().split('\n')

    def do_exit(self, _) -> None:
        """ Exit console.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def do_quit(self, _) -> None:
        """ Exit console.

        :return None: None
        :raises EOFError: EOF error
        """

        raise EOFError

    def do_clear(self, _) -> None:
        """ Clear terminal window.

        :return None: None
        """

        self.print_empty('%clear', end='')

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

        for command in sorted(self.shorts):
            alias = self.shorts[command][0].split()[0]

            if alias in self.internal:
                data['core'].append((command, self.shorts[command][1]))
                continue

            alias = self.external.get(alias, None)
            if not alias:
                continue

            data[alias['Category']].append(
                (command, self.shorts[command][1]))

        buffer = ''

        for category in sorted(data):
            with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
                self.print_table(f"{category} Commands", headers, *data[category])
                buffer += buf.getvalue()

        self.print_empty(buffer, end='')

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

    def verify_args(self, args: list, info: dict) -> None:
        """ Check if arguments correct for command.

        :param list args: list of args
        :param dict info: dictionary of command info
        :return None: None
        """

        if not info['Options']:
            if len(args) - 1 < info['MinArgs']:
                self.print_usage(info['Usage'])
                return

            if info['Method'](args):
                self.print_usage(info['Usage'])
            return

        epilog = None
        if 'Examples' in info:
            epilog = "examples:\n  "
            epilog += "\n  ".join(info['Examples'])

        parser = argparse.ArgumentParser(
            prog=args[0],
            description=info['Description'],
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=epilog
        )

        for entry in info['Options']:
            parser.add_argument(*entry[0], **entry[1])

        try:
            if len(args) - 1 < info['MinArgs']:
                parser.print_help()
                return

            if info['Method'](parser.parse_args(args[1:])):
                parser.print_help()

        except SystemExit:
            return

    def loop(self) -> None:
        """ Run main loop.

        :return None: None
        """

        self.preloop()

        if self.intro:
            self.print_empty(self.intro)

        while True:
            try:
                for name, completer in self.dynamic_complete.items():
                    self.complete[name] = completer()

                if not self.source:
                    with patch_stdout(raw=True):
                        line = self._session.prompt(
                            ANSI(self.prompt), completer=NestedCompleter.from_nested_dict(self.complete))
                else:
                    line = self.source.pop(0)

                if line is None:
                    break

                line = line.strip()

                if not line:
                    self.emptyline()
                    continue

                line = self.precmd(line)
                line = self.onecmd(line)
                self.postcmd(line)

            except EOFError:
                self.print_empty(end='')
                break

            except KeyboardInterrupt:
                self.print_empty(end='')
                continue

            except RuntimeError as e:
                self.print_error(str(e))

            except RuntimeWarning as w:
                self.print_warning(str(w))

            except Exception as e:
                self.print_error(f"An error occurred: {str(e)}!")
                traceback.print_exc(file=sys.stdout)

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

    def precmd(self, line: str) -> str:
        """ Do something before executing command.

        :param str line: command line
        :return str: command
        """

        return line

    def postcmd(self, line: str) -> None:
        """ Do something after command execution.

        :param str line: command line
        :return None: None
        """

        return

    def onecmd(self, line: str) -> str:
        """ Execute single command.

        :param str line: line
        :return str: command result
        """

        try:
            args = shlex.split(line)

        except ValueError as e:
            self.print_error(f"Error parsing command: {str(e)}")

        if len(args) < 1:
            return line

        for builtin, func in self.builtins.items():
            if args[0].startswith(builtin):
                first = args[0].lstrip(builtin)
                prepend = []

                if not isinstance(func, str):
                    if first:
                        func([first, *args[1:]])
                    else:
                        func(args[1:])

                    return line

                if first:
                    args = [func, first, *args[1:]]
                else:
                    args = [func, *args[1:]]

        if args[0] not in self.external \
                and args[0] not in self.internal \
                and args[0] in self.shorts:
            short = self.shorts[args[0]]
            command = short[0]

            for i, arg in enumerate(args):
                command = command.replace(f'?{i}', arg)

            argv = shlex.split(command)
            args = []

            for arg in argv:
                if not arg.startswith('?'):
                    args.append(arg)

        if args[0] not in self.external \
                and args[0] in self.internal:
            getattr(self, 'do_' + args[0])(args)
            return line

        status, name = self.verify_command(args)

        if status:
            fixed = [name, *args[1:]]
            command = self.external[name]

            self.verify_args(fixed, command)
            return ' '.join(fixed)

        if name is not None:
            self.print_warning(f"Did you mean? {', '.join(name)}")

        self.default(args)
        return line

    def emptyline(self) -> None:
        """ Do something on empty line.

        :return None: None
        """

        return

    def default(self, args: list) -> Any:
        """ Failure handle.

        :param list args: list of args
        :return Any: command result
        """

        self.print_error(f"Unrecognized command: {args[0]}")
