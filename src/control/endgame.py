from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import Screen
from kivy.app import App

from lib.config import Configuration


class EndGame(Screen):
    score = NumericProperty(0)
    highscore = NumericProperty(0)
    highscorer = StringProperty("")
    has_highscore = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if Configuration.highscores:
            self.has_highscore = True
            self.highscorer, self.highscore = Configuration.highest_score
        if Configuration.name:
            self.name_input.text = Configuration.name

    def update(self, score):
        self.score = score

    def save_game(self):
        self.has_highscore = True
        if self.name_input.text:
            Configuration.name = self.name_input.text
        if Configuration.is_highscore(self.score):
            Configuration.register_highscore(self.name_input.text, self.score)
        if Configuration.is_highest_score(self.score):
            self.highscorer, self.highscore = Configuration.highest_score
        Configuration.save()

    def on_restart_clicked(self):
        self.save_game()
        App.get_running_app().play_game()

    def on_menu_clicked(self):
        self.save_game()
        App.get_running_app().go_home()