import kivy

kivy.require('1.10.1')

from kivy.app import App
from kivy.clock import Clock

from src.game import TractaGame
from src.space import Debris
from src.ship import Ship, Beam

class TractaApp(App):
    def build(self):
        game = TractaGame()
        Clock.schedule_interval(game.tick, 1.0/60)
        return game


TractaApp().run()
