# Badges

[![Developer](https://img.shields.io/badge/developer-EntySec-blue.svg)](https://entysec.com)
[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://github.com/EntySec/Badges)
[![Forks](https://img.shields.io/github/forks/EntySec/Badges?style=flat&color=green)](https://github.com/EntySec/Badges/forks)
[![Stars](https://img.shields.io/github/stars/EntySec/Badges?style=flat&color=yellow)](https://github.com/EntySec/Badges/stargazers)
[![CodeFactor](https://www.codefactor.io/repository/github/EntySec/Badges/badge)](https://www.codefactor.io/repository/github/EntySec/Badges)

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
