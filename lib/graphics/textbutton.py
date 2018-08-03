from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.label import Label


class TextButton(Label):
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