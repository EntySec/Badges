# Badges

[![Developer](https://img.shields.io/badge/developer-EntySec-blue.svg)](https://entysec.com)
[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://github.com/EntySec/Badges)
[![Forks](https://img.shields.io/github/forks/EntySec/Badges?style=flat&color=green)](https://github.com/EntySec/Badges/forks)
[![Stars](https://img.shields.io/github/stars/EntySec/Badges?style=flat&color=yellow)](https://github.com/EntySec/Badges/stargazers)
[![CodeFactor](https://www.codefactor.io/repository/github/EntySec/Badges/badge)](https://www.codefactor.io/repository/github/EntySec/Badges)

Badges is a Python3 library that is used for advanced and intuitive printing.

## Features

* Support for different colors using [ColorScript](https://github.com/EntySec/ColorScript) commands.
* Map plotting that enables you to point on a specific place on an ASCII map.
* Logging support, if logging is enabled, you can log all the messages to the file.

## Installation

```
pip3 install git+https://github.com/EntySec/Badges
```

## Examples

### Status messages

```python3
from badges import Badges

badges = Badges()
reply = badges.input_question("Do it [y/N]: ")

if reply.lower() in ['y', 'yes']:
    badges.print_process("Doing it...")
else:
    badges.print_warning("Not doing it.")
```

<details>
    <summary>Result</summary><br>
    <pre>
[?] Do it [y/N]: y
[*] Doing it...</pre>
</details>

### Map plotting

```python3
from badges import Badges

plot = Map()
plot.deploy(55.751244, 37.618423)

print(plot.get_map())
```

<details>
    <summary>Result</summary><br>
    <pre>
                       . _..::__:  ,-"-"._       |7       ,     _,.__
       _.___ _ _<_>`!(._`.`-.    /        _._     `_ ,_/  '  '-._.---.-.__
     .{     " " `-==,',._\{  \  / {)     / _ ">_,-' `                .--?_
      \_.:--.       `._ )`^-. "'      , [_/(                       __,/-'
     '"'     \         "    _L       oD_,--' *              )     /. (|
              |           ,'         _)_.\\._<> 6              _,' /  '
              `.         /          [_/_'` `"(                <'}  )
               \\    .-. )          /   `-'"..' `:._          _)  '
        `        \  (  `(          /         `:\  > \  ,-^.  /' '
                  `._,   ""        |           \`'   \|   ?_)  {\
                     `=.---.       `._._       ,'     "`  |' ,- '.
                       |    `-._        |     /          `:`<_|h--._
                       (        >       .     | ,          `=.__.`-'\
                        `.     /        |     |{|              ,-.,\     .
                         |   ,'          \   / `'            ,"     \
                         |  /             |_'                |  __  /
                         | |                                 '-'  `-'   \.
                         |/                                        "    /
                         \.                                            '</pre>
</details>

### Tables

```python3
from badges import Tables

tables = Tables()
tables.print_table('Table 1', ('ID', 'Name'), ('111', 'Ivan Nikolskiy'))
```

<details>
    <summary>Result</summary><br>
    <pre>
Table 1:<br>
    ID     Name
    111    Ivan Nikolskiy</pre>
</details>
