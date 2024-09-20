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

from badges.cmd import Cmd, Command


class CLI(Cmd):
    def __init__(self) -> None:
        super().__init__(
            prompt='%red$ %end',
            intro="""
%bold%whiteSample Command-Line Interface%end
""",
        )

        self.commands = [
            Command({
                'Name': "sample",
                'Category': "test",
                'Description': "Sample command with no args.",
                'Usage': "sample <option>",
                'MinArgs': 1,
                'Method': self.sample
            }),
            Command({
                'Name': "sample1",
                'Category': "test",
                'Description': "Sample command with args.",
                'MinArgs': 1,
                'Options': [
                    (
                        ('-o', '--option'),
                        {
                            'help': "Option to use.",
                        }
                    )
                ],
                'Method': self.sample1,
                'Examples': [
                    "sample1 -o option1",
                    "sample1 --option option1"
                ],
                'Shorts': {
                    'sample2': ['sample1 -o ?1', 'Sample2']
                }
            })
        ]

        self.add_external(self.commands)

    def sample(self, args: list) -> None:
        self.print_information(args[1])

    def sample1(self, args) -> None:
        self.print_information(args.option)


if __name__ == '__main__':
    cli = CLI()
    cli.loop()
