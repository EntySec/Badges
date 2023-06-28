# Badges

<p>
    <a href="https://entysec.com">
        <img src="https://img.shields.io/badge/developer-EntySec-blue.svg">
    </a>
    <a href="https://github.com/EntySec/Badges">
        <img src="https://img.shields.io/badge/language-Python-blue.svg">
    </a>
    <a href="https://github.com/EntySec/Badges/stargazers">
        <img src="https://img.shields.io/github/stars/EntySec/Badges?color=yellow">
    </a>
</p>

Badges is a Python3 library that is used for advanced and intuitive printing.

## Features

* Support for different colors using [ColorScript](https://github.com/EntySec/ColorScript) commands.
* Localization support, all messages can be translated on-fly using online services.
* Logging support, if logging is enabled, you can log all the messages to the file.

## Installation

```
pip3 install git+https://github.com/EntySec/Badges
```

## Examples

```python3
from badges import Badges

badges = Badges(lang='ru', dictionary='/home/parrot/l10n.txt')
badges.print_success("Hello, world!")
```
