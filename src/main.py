import kivy
from kivy.lang import Builder

kivy.require('1.10.1')
Builder.load_file('./ui/tracta.kv')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from src.game import TractaGame, GameScreen
from src.game.ship import Ship, Beam
from src.game.space import Debris

from src.control import MainMenu, MenuButton


class TractaApp(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.screen_manager.add_widget(MainMenu(name="menu"))
        self.screen_manager.add_widget(GameScreen(name="game"))
        #game.start()
        return self.screen_manager

    def play_game(self):
        self.screen_manager.current = "game"
        self.screen_manager.get_screen("game").start()

TractaApp().run()
