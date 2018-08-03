from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ColorProperty

from lib.geometry import Point, Velocity, Vector, Momentum, Displacement
from lib.graphics.scale import Scale


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
    size = NumericProperty(100)
    default_colour = 0.6, 0.65, 1, 0.5
    colour = ColorProperty(default_colour)
    destroyed: bool = False
    mass = NumericProperty(100)

    def __init__(self, position: Vector, rotation: int = 0, size: int = 100, **kwargs):
        super().__init__(**kwargs)
        self.center = tuple(position)
        self.rotation = rotation
        self.size = size * Scale.width_factor # Scales to screen size
        self.mass = size

    def highlight(self, colour=(0.8, 0.9, 1, 0.6)):
        self.colour = colour

    def remove_highlight(self):
        self.colour = self.default_colour

    @property
    def position(self):
        return Point(self.center_x, self.center_y)

    @position.setter
    def position(self, pos: Point):
        self.center_x, self.center_y = pos

    def move(self, dt=1, ds=0) -> Displacement:
        displacement = self.velocity.to_displacement(dt)
        self.center_x += displacement.x
        self.center_y += displacement.y - ds
        return displacement

    def destruct(self, t=0.2):
        self.destroyed = True
        anim = Animation(a=0, duration=t)
        anim.start(self.canvas.children[1])

    @property
    def points(self):
        return (
                    Point(*point).rotate_about(Point(*self.center), self.rotation)
                    for point in zip(self.canvas.children[3].points[::2], self.canvas.children[3].points[1::2])
        )