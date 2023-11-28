# pyldplayer
python wrapper for ldplayer

## Installation
```bash
pip install pyldplayer
```

## usage
you can refer to [cli doc](https://www.ldplayer.net/blog/introduction-to-ldplayer-command-line-interface.html) for all options

in addition, this library also supports loading record, keyboard mapping into pydantic dataclasses
```py
from time import sleep
from pyldplayer.autogui.player import LDAutoPlayer
from pyldplayer.console.player import LDConsolePlayer

console = LDConsolePlayer(path)
auto = LDAutoPlayer(x)

cinstance = console[3]
cinstance.launch()

sleep(2)

autoinstance = auto["some name"]
autoinstance.fullscreen()
```

## changelog
* fixed instance will be terminated if script ended
* fixed unsanitized query results
* fully documented
