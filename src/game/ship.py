import math as maths

from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.graphics.vertex_instructions import Triangle

from lib.geometry import Point, Velocity, Vector, Momentum, Displacement
from src.game.space import SpaceObject, Debris


class Beam(Widget):
    _refresh_event = None
    bredth = 67
    energy = maths.tau
    target = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.triangle = Triangle()

    def shine(self, position: Vector):
        self.show(position)
        for debris in self.parent.parent.debris:
            hit_rate = self.hits(debris)
            if hit_rate:
                debris.highlight()
                self.pull(debris, hit_rate)
            else:
                debris.remove_highlight()

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

    def pull(self, debris, strength=1.0):
        displacement = debris.position - self.base
        p_magnitude = maths.sqrt(2*(self.parent.mass+debris.mass)*self.energy) * strength
        momentum = Momentum.from_vector(displacement.fit_unit_circle() * p_magnitude)
        self.parent.momentum += momentum
        debris.momentum -= momentum

    @property
    def base(self):
        return self.parent.middle

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
        return ((self.vector + offset).angle - self.vector.angle) % 360  # abs didn't work because bearings

    def hits(self, debris):
        hits = 0
        for point in debris.target_points:
            displacement = point - self.base
            if self.angle - self.angle_width < displacement.angle < self.angle + self.angle_width \
                    and displacement.length < self.radius:
                hits += 1
        return hits / len(list(debris.points))

    def end(self):
        self.refresh_event.cancel()
        if self.triangle in self.canvas.children:
            self.canvas.remove(self.triangle)

        for debris in self.parent.parent.debris:
            debris.remove_highlight()

    def poll(self, pos: Point, freq=1.0/60):
        try:
            self.refresh_event.cancel()
        except AttributeError:
            pass
        self.refresh_event = Clock.schedule_interval(lambda dt: self.shine(pos), freq)


class Ship(SpaceObject):
    velocity = Velocity(x=0, y=0)
    distance = NumericProperty(0)
    size = 150, 150
    health = NumericProperty(3)
    mass = NumericProperty(50)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def move(self, dt=1) -> Displacement:
        displacement = self.velocity.to_displacement(dt)
        self.center_x += displacement.x
        self.distance += displacement.y
        return displacement

    def correct_image(self):
        self.image.texture.mag_filter = 'nearest'
        self.image.size = self.size
        self.image.center = self.center

    def seek(self, x):
        self.velocity = self.velocity + Velocity((x - self.center_x)/100, 0)

    def collides_with(self, debris: Debris):
        for point in debris.target_points:
            if (point - self.middle).length < self.radius:
                return True

    @property
    def radius(self):
        return sum(self.size) // 4 #2.5

    @property
    def middle(self):
        return Point(self.center_x, self.center_y)