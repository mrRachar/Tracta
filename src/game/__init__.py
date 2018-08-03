import random

from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty

from lib.geometry import Point, collision_velocity, Velocity
from lib.graphics.scale import Scale
from src.game.space import Debris


class TractaGame(Widget):
    ship = ObjectProperty(None)
    debris = ListProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.size = Window.size
        self.ship.correct_image()
        self.debris = []

        # Generate debris
        self.add_debris(Debris(Point.random(x_range=(0, self.width), y_range=(self.height * 4/5, self.height))))
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
                self.ship.health -= (debris.mass // 40) / 2 or 0.5

        self.manage_debris_field()

        if  self.ship.x < 0 or self.ship.right > self.width:
            self.ship.velocity = self.ship.velocity.flip_x()

    def manage_debris_field(self):
        # Create debris on the fly
        if max(debris.position.y for debris in self.debris) <= self.height+10:
            for x_range in ((0, self.width/4), (0, self.width/3), (0, self.width), (self.width * 2/3, self.width), (self.width * 3/4, self.width)):
                self.add_debris(Debris(
                    Point.random(x_range=x_range, y_range=(self.height,self.height + self.height / (1.2 * Scale.proportional_factor ** 1.2))),
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

    @property
    def is_over(self):
        return self.ship.health <= 0


class GameManager(Screen):
    game = None
    event = None
    endgame = None

    def start(self):
        self.game = TractaGame()
        self.add_widget(self.game)
        self.event = Clock.schedule_interval(self.game.tick, 1.0/60)
        self.endgame = Clock.schedule_interval(self.check_end, 1.0/60)

    def check_end(self, dt):
        if self.game.is_over:
            self.end()

    def end(self):
        self.game.ship.health = 0
        self.event.cancel()
        self.endgame.cancel()

        def callback(dt):
            self.remove_widget(self.game)
            App.get_running_app().show_endgame(round(self.game.ship.distance/10, 1))
            self.game = None
        Clock.schedule_once(callback, 1)