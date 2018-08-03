from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App


class AboutScreen(Screen):
    about_text = """
Created by Matthew Ross Rachar 

Programmed by Matthew Ross Rachar

Graphics by Matthew Ross Rachar

with thanks to Ælfi the Cat
[size=18]He's often sleeping behind me when I solve
bugs so maybe he's helping?[/size] 
[size=15][he also sleeps there when I can't so maybe it's nothing][/size]

Programmed in Python 3.6
[size=18]with many thanks to the Python Software Foundation
and to the BDFL for his years of service[/size]

Game built with Kivy 1.10.1
[size=18]with thanks to people over at kivy.org[/size]

Graphics designed in Piskel

Supported By
[size=22]No one[/size]
    """

    def on_back_clicked(self):
        App.get_running_app().go_home()