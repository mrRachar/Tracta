from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App


class EndGame(Screen):
    score = NumericProperty(0)
    def on_restart_clicked(self):
        App.get_running_app().play_game()

    def on_menu_clicked(self):
        App.get_running_app().go_home()