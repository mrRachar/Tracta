from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App


class ScoresScreen(Screen):
    def update(self):
        pass

    def on_back_clicked(self):
        App.get_running_app().go_home()