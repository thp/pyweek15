#!/usr/bin/env python

from src.engine.app import App
from src.scenes.game import Game

app = App(title="One Whale Trip", resolution=(800, 480), scenes=[Game])
app.run()
