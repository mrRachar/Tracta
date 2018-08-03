from kivy.core.window import Window
from kivy.config import Config

class _ScaleMeta(type):
    @property
    def width_factor(cls, strength=1):
        return Window.width / cls.base_width

    @property
    def height_factor(cls, strength=1):
        return Window.height / cls.base_height

    @property
    def proportional_factor(cls):
        return cls.height_factor / cls.width_factor


class Scale(metaclass=_ScaleMeta):
    base_width = 800
    base_height = 600