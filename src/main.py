import kivy
from kivy.lang import Builder

kivy.require('1.10.1')
Builder.load_file('./ui/tracta.kv')

from kivy.app import App
from kivy.clock import Clock

from src.game import TractaGame
from src.game.ship import Ship, Beam
from src.game.space import Debris

class TractaApp(App):
    def build(self):
        game = TractaGame()
        Clock.schedule_interval(game.tick, 1.0/60)
        return game


TractaApp().run()
