from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App


class AboutScreen(Screen):
    about_text = """
We do things
I think
Lot's of things
Maybe not
Who knows
We could if we wanted I guess
Lines
Lines of text
Lorem Ipsum is for weaklings
I will write enough lines of text
They may not be interesting
(They may though,
I do doubt it)
But they will be enough
And if they aren't
I'll have to write some more
Some more text to fill up the lines

Anyway, about us:
We do things
I think
Lot's of things
Maybe not
Who knows
We could if we wanted I guess
Lines
Lines of text
Lorem Ipsum is for weaklings
I will write enough lines of text
They may not be interesting
(They may though,
I do doubt it)
But they will be enough
And if they aren't
I'll have to write some more
Some more text to fill up the lines
    """

    def on_back_clicked(self):
        App.get_running_app().go_home()