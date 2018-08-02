import random

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

from src.geometry import Point, Velocity, collision_velocity
from src.space import Debris


class TractaGame(Widget):
    ship = ObjectProperty(None)
    debris = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = Window.size
        self.add_debris(Debris(Point.random(x_range=(0, self.width), y_range=(self.height * 3/4, self.height * 5/6))))
        #self.debris[0].highlight()
        for x_range in ((0, self.width * 1/3), (self.width * 2/3, self.width)):
            for _ in range(2):
                self.add_debris(Debris(Point.random(x_range=x_range, y_range=(0, self.height)), rotation=random.randint(0, 359)))

    def add_debris(self, debris):
        self.debris.append(debris)
        self.add_widget(debris)

    def remove_debris(self, debris):
        try:
            self.debris.remove(debris)
        except ValueError:
            try:
                self.remove_widget(debris)
            except ValueError:
                pass

    def tick(self, dt):
        _, ds = self.ship.move(dt)

        for debris in self.debris:
            debris.move(dt, ds)
            if self.ship.collides_with(debris) and not debris.destroyed:
                s_v = self.ship.velocity
                self.ship.velocity = collision_velocity(self.ship.mass, debris.mass/6, self.ship.velocity, debris.velocity)
                debris.destruct(t=0.5)
                self.remove_debris(debris)
                self.ship.health -= (debris.mass // 50) / 2 or 0.5

        self.manage_debris_field()

        if  self.ship.x < 0 or self.ship.right > self.width:
            self.ship.velocity = self.ship.velocity.flip_x()

    def manage_debris_field(self):
        # Create debris on the fly
        if max(debris.position.y for debris in self.debris) <= self.height+10:
            for x_range in ((0, self.width/4), (0, self.width/3), (0, self.width), (self.width * 2/3, self.width), (self.width * 3/4, self.width)):
                self.add_debris(Debris(
                    Point.random(x_range=x_range, y_range=(self.height,2*self.height)),
                    rotation=random.randint(0, 359),
                    size=random.randint(40, 150)
                ))

        # Remove debris, which is out of range
        for debris in self.debris:
            if not -debris.size*2 < debris.position.x < self.width + debris.position.x*2 \
                    or debris.position.y < -self.height:
                self.remove_debris(debris)


    def on_touch_down(self, touch):
        self.ship.beam.shine(touch)
        self.ship.beam.poll(touch)
        return True

    def on_touch_move(self, touch):
        self.ship.beam.poll(touch)

    def on_touch_up(self, touch):
        self.ship.beam.end()
        return True
