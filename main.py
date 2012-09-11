#!/usr/bin/env python
"""
Usage: main [ ( -l <level> | -s <scene> ) ]

Options:
    -l, --level <level>  start with level x
    -s, --scene <scene>  start with scene x
"""
from src.engine.app import App
from src.scenes.game import Game
from src.scenes.menu import MainMenu

from docopt import docopt
arguments = docopt(__doc__)

app = App(title="One Whale Trip",
          resolution=(800, 480),
          scenes=[MainMenu, Game],
          entry=arguments['--scene'] or "Game"
          )
app.run()
