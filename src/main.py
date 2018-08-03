import os, sys

# Set cwd to root of project (as code paths based around there)
if os.getcwd().endswith("src"):
    os.chdir('../')
    sys.path.append('./')

import kivy
from kivy.lang import Builder

kivy.require('1.10.1')
Builder.load_file('src/ui/tracta.kv')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from src.game import GameManager
from src.game.ship import Ship, Beam
from src.game.space import Debris

from src.control import MainMenu
from src.control.about import AboutScreen
from src.control.scores import ScoresScreen
from src.control.endgame import EndGame

from lib.graphics.textbutton import  TextButton
from lib.graphics.paragraph import Paragraph


class TractaApp(App):
    def build(self):
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.screen_manager.add_widget(MainMenu(name='menu'))
        self.screen_manager.add_widget(GameManager(name='game'))
        self.screen_manager.add_widget(ScoresScreen(name='scores'))
        self.screen_manager.add_widget(AboutScreen(name='about'))
        self.screen_manager.add_widget(EndGame(name='endgame'))
        self.icon = 'rsc/ship8.ico'
        return self.screen_manager

    def play_game(self):
        self.screen_manager.current = 'game'
        self.screen_manager.get_screen('game').start()

    def show_about(self):
        self.screen_manager.current = 'about'

    def show_scores(self):
        self.screen_manager.current = 'scores'
        self.screen_manager.get_screen('scores').update()

    def go_home(self):
        self.screen_manager.current = 'menu'

    def show_endgame(self, score):
        self.screen_manager.current = 'endgame'
        self.screen_manager.get_screen('endgame').update(score)

TractaApp().run()
