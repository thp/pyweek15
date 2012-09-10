#!/usr/bin/env python

from src.engine.app import App
from src.scenes.game import Game

app = App(title="PyWeek 15", resolution=(800, 480), scenes=[Game])
app.run()
