from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_play_clicked(self):
        App.get_running_app().play_game()

    def on_scores_clicked(self):
        App.get_running_app().show_scores()

    def on_about_clicked(self):
        App.get_running_app().show_about()
