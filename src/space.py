from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

from src.geometry import Point, Velocity, Vector, Momentum


class SpaceObject(Widget):
    velocity: Velocity
    mass: int

    @property
    def momentum(self):
        return self.velocity.to_momentum(self.mass)

    @momentum.setter
    def momentum(self, p: Momentum):
        self.velocity = p.to_velocity(self.mass) # not +=


class Debris(SpaceObject):
    rotation = NumericProperty(0)
    velocity = Velocity()
    size = 100
    mass = NumericProperty(100)

    def __init__(self, position: Vector, rotation: int = 0, size: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.center = tuple(position)
        self.rotation = rotation

    @property
    def position(self):
        return Point(self.center_x, self.center_y)

    def move(self):
        self.center_x += self.velocity.x
        self.center_y += self.velocity.y

    @property
    def points(self):
        return (Point(*point) for point in zip(self.canvas.children[3].points[::2], self.canvas.children[3].points[1::2]))