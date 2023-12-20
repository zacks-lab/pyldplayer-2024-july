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
from pyldplayer import LDAutoGui
from pyldplayer import LDConsole

x = LDConsole("xxxxxxxxxxxxxxxxxxxxx")
autox = LDAutoGui(x)

w = x[3]
w.launch()
autow = autox.waitFor(3)
autow.screenshot()

oprr = autow.operationRecorder()
oprr.runScript(3)
```

## changelog
* fixed instance will be terminated if script ended
* fixed unsanitized query results
* fully documented
