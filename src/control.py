from kivy.core.window import Window
from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.app import App


class MenuButton(Label):
    font_colour = ColorProperty((1, 1, 1, 1))
    press_colour = ColorProperty((0.7, 0.9, 0.9, 1))
    command = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__pressed = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.color = self.press_colour
            self.__pressed = True
            return True

    def on_mouse_pos(self, *args):
        pass

    def on_touch_up(self, touch):
        if self.__pressed and self.collide_point(*touch.pos):
            self.command()
        self.__pressed = False
        self.color = self.font_colour


class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_play_clicked(self):
        App.get_running_app().play_game()

    def on_scores_clicked(self):
        App.get_running_app().show_scores()

    def on_about_clicked(self):
        App.get_running_app().manager.show_about()