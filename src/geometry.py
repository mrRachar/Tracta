import random
import math as maths
from numbers import Number
from typing import NamedTuple, Iterable
from abc import ABC


def atan(q):
    return maths.degrees(maths.atan(q))

def tan(q):
    return maths.tan(maths.radians(q))

def cos(q):
    return maths.cos(maths.radians(q))

def sin(q):
    return maths.sin(maths.radians(q))

def bearing(x, y):
    if y == 0:
        return ((x >= 0) - (x < 0)) * 90
    angle = atan(x/y)
    if y < 0:
        angle += 180
    if angle < 0:
        angle += 360
    return angle


class Vector:
    __x: int
    __y: int

    def __init__(self, x: Number=0, y: Number=0):
        self.__x = x
        self.__y = y

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x},{self.y})"

    def __iter__(self):
        yield self.x
        yield self.y

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    @property
    def angle(self):
        """Bearing style angle of vector from base"""
        return bearing(self.x, self.y)

    @property
    def length(self):
        return maths.sqrt(self.x**2 + self.y**2)

    def __sub__(self, other):
        return self.__class__(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return self.__class__(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(self.x * other, self.y * other)
        elif isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, tuple):
            return self * Vector(*other)
        else:
            raise TypeError

    def __truediv__(self, other):
        return self * (1/other)

    def fit_unit_circle(self):
        return self / self.length

    def flip_x(self):
        return self.__class__(self.x * -1, self.y)

    def flip_y(self):
        return self.__class__(self.x, self.y * -1)

    def flip(self):
        return -self

    @classmethod
    def from_vector(cls, vector):
        return cls(*vector)

    def rotate(self, angle: Number):
        x = self.x * cos(angle) - self.y * sin(angle)
        y = self.x * sin(angle) + self.y * cos(angle)
        return self.__class__(x, y)

    @property
    def modulus_argument_form(self):
        return f"{self.__class__.__name__}<{self.length}, θ={self.angle}>"


class Point(Vector):
    @classmethod
    def random(cls, x=None, y=None, x_to=500, y_to=500):
        return cls(x or random.randint(0, x_to), y or random.randint(0, y_to))


class Velocity(Vector):
    def to_momentum(self, mass):
        return Momentum.from_vector(self * mass)

    def to_displacement(self, time):
        return Displacement.from_vector(self * time)

    @property
    def speed(self):
        return self.length


class Momentum(Vector):
    def to_velocity(self, mass):
        return Velocity.from_vector(self / mass)


class Displacement(Vector):
    pass


class Line:
    gradient: int
    offset: int

    def __init__(self, gradient, offset=0):
        self.gradient = gradient
        self.offset = offset

    @classmethod
    def from_points(cls, a, b):
        m = (a.y-b.y)/(a.x-b.x)
        k = a.y - a.x * m
        return cls(m, k)

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.gradient}*x {self.offset:+}>"

    def __lt__(self, point: Point):
        return point.y > self(point.x)

    def __eq__(self, point: Point):
        return point.y == self(point.x)

    def __gt__(self, point: Point):
        return point.y < self(point.x)

    def __call__(self, x):
        return self.apply(x)

    def apply(self, x):
        return (self.gradient * x) + self.offset

    @property
    def sign(self):
        return self.gradient > 0 - self.gradient < 0


class GeometricShape(ABC):
    points: Iterable[Point]