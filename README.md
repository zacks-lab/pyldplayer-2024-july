see https://github.com/ZackaryW/pyldplayer

# pyldplayer
this module provides all the necessary interfaces to interact with LDPlayer app

NOTE: since v2.0, the module will not contain any automation functionalities, you should refer to `autoldplayer` module instead

## Installation
```
pip install pyldplayer
```

## Usage
```py
from pyldplayer.console import Console
from pyldplayer.process import DefaultProcess
from pyldplayer.windows import WindowMgr

x = DefaultProcess("{path}")
w = Console(x)

k = w.list2()

# launch in root mode
k[0].modify(root=True)
k[0].launch()
k[0].refresh()
```

## Features
### Layer 1: Process
* communicates directly with the LDConsole.exe cli using `process.BaseProcess`
> this is the only way to interact with the app through command line interfaces
* `process.BaseProcess` is implemented on top of `process.BaseProcessInterface` and integrated `process.ProcessVerifier`
* `process.CachedProcess` is both an example of extending features to the `process.BaseProcess` and a way to cache executed commands
* `process.ProcessVerifier` checks if the path is valid

### Layer 2: Console
* `Console` provides all CLI APIs
* `Console.list2` returns a list of `ConsoleInstance` objects

### Layer 3: Files
* `ConfigMgr` and `KmpMgr` provide access to `config` and `kmp` files, as well as loading them into pydantic models
* `LeidianCfg` for instanced config
* `LeidiansCfg` for host config

### Layer 4: Windows
* Provides `pygetwindow` related functions
> This allows the following
- window orientation `WindowMgr.orientation`
- window resizing `WindowMgr.resize`

### Optional
* contains extended and optional implementations 
> `pyautogui` is needed for some features

## Required dependencies
- `pygetwindow`
- `screeninfo`
- `pydantic`

## Official Documentations
[cli doc](https://www.ldplayer.net/blog/introduction-to-ldplayer-command-line-interface.html)
