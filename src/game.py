import random

from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from src.geometry import Point, Velocity
from src.space import Debris


class TractaGame(Widget):
    ship = ObjectProperty(None)
    debris = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = Window.size
        for _ in range(5):
            self.add_debris(Debris(Point.random(x_to=self.width, y_to=self.height), random.randint(0, 359)))

    def add_debris(self, junk):
        self.debris.append(junk)
        self.add_widget(junk)

    def tick(self, dt):
        _, ds = self.ship.move(dt)

        for debris in self.debris:
            debris.move(dt, ds)

        if  self.ship.x < 0 or self.ship.right > self.width:
            self.ship.velocity = self.ship.velocity.flip_x()

    def on_touch_down(self, touch):
        self.ship.beam.shine(touch)
        self.ship.beam.poll(touch)
        return True

    def on_touch_move(self, touch):
        #self.ship.beam.shine(touch)
        self.ship.beam.poll(touch)
        #self.ship.seek(touch.x)

    def on_touch_up(self, touch):
        self.ship.beam.end()
        return True
