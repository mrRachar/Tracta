from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics.vertex_instructions import Triangle

from src.geometry import Point, Velocity, Vector, Momentum
from src.space import SpaceObject


class Beam(Widget):
    _refresh_event = None
    bredth = 67

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.triangle = Triangle()

    def shine(self, position: Vector):
        self.show(position)
        for debris in self.parent.parent.debris:
            hit_rate = self.hits(debris)
            if hit_rate:
                self.pull(debris, hit_rate)

    def show(self, position: Vector):
        self.target = Point(position.x, position.y)
        offset = (self.target - self.base).rotate(-90).fit_unit_circle() * self.bredth
        self.triangle.points = [
                *self.base,
                *(self.target+offset),
                *(self.target-offset)
        ]

        if self.triangle not in self.canvas.children:
            self.canvas.add(self.triangle)

    def pull(self, debris, strength=1):
        displacement = debris.position - self.base
        momentum = Momentum.from_vector(displacement.fit_unit_circle() * strength * 10)
        self.parent.momentum += momentum
        debris.momentum -= momentum

    @property
    def base(self):
        return Point(self.center_x+28, self.center_y+28)

    @property
    def radius(self):
        return self.vector.length

    @property
    def vector(self):
        return self.target - self.base

    @property
    def angle(self):
        return self.vector.angle

    @property
    def angle_width(self):
        offset = (self.target - self.base).rotate(-90).fit_unit_circle() * self.bredth
        return abs((self.vector + offset).angle - self.vector.angle)

    def hits(self, debris):
        hits = 0
        for point in debris.points:
            displacement = point - self.base
            if self.angle - self.angle_width < displacement.angle < self.angle + self.angle_width \
                    and displacement.length < self.radius:
                hits += 1
        return hits / len(list(debris.points))

    def end(self):
        if self.triangle in self.canvas.children:
            self.canvas.remove(self.triangle)
        self.refresh_event.cancel()

    def poll(self, pos: Point, freq=1.0/60):
        try:
            self.refresh_event.cancel()
        except AttributeError:
            pass
        self.refresh_event = Clock.schedule_interval(lambda dt: self.show(pos), freq)


class Ship(SpaceObject):
    velocity = Velocity(x=0, y=0)
    distance = NumericProperty(0)
    size = 150, 150
    health = NumericProperty(42)
    mass = NumericProperty(1000)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move(self):
        self.center_x += self.velocity.x
        self.distance += self.velocity.y

    def seek(self, x):
        self.velocity = self.velocity + Velocity((x - self.center_x)/100, 0)