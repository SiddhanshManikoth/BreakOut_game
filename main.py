from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
import keyboard
import time

Builder.load_string(""" 
<Game>
    

""")


class Ball(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class Brick(Widget):
    pass


class Pad(Widget):

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_x - self.center_x) / (self.height / 2)
            bounced = Vector(vx, -1 * vy)
            vel = bounced
            ball.velocity = vel.x + offset, vel.y


class Game(FloatLayout):
    ball = ObjectProperty(None)
    pad = ObjectProperty(None)
    brick_list = []
    lives = 6
    cleared = False

    for n in range(24):
        brick = ObjectProperty(None)
        brick_list.append(brick)

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.ball = self.ids['ball']
        self.ball.size = 20, 20
        self.pad = self.ids['pad']
        for brick in self.brick_list:
            id = (self.brick_list.index(brick))
            self.brick_list[id] = Brick()
        brick_x = 0
        brick_y = 350
        for brick in self.brick_list:
            brick.id = (self.brick_list.index(brick))
            brick.size_hint_x = None
            brick.size_hint_y = None
            brick.size = 95, 30
            if brick_x <= 600:
                brick.pos = brick_x, brick_y
                brick_x += 100
            else:
                brick.pos = brick_x, brick_y
                brick_y += 35
                brick_x = 0
        for brick in self.brick_list:
            print(brick.pos)
            self.add_widget(brick)
        Window.bind(on_key_down=self.input_listeners)

    def destroy_brick(self, ball, brick):
        if ball.collide_widget(brick):
            self.brick_list.remove(brick)
            self.remove_widget(brick)
            ball.velocity_y *= -1.1

    def input_listeners(self, *args):

        if keyboard.is_pressed("left"):
            self.pad.pos[0] += -20
        if keyboard.is_pressed("right"):
            self.pad.pos[0] += 20

    def update(self, dt):
        self.ball.move()
        # bounce off top
        if self.ball.y > self.height:
            self.ball.velocity_y *= -1
        if self.ball.y < 0:

            if self.lives > 0:
                time.sleep(3)
                self.serve_ball()
                self.pad.pos = 400, 0
                self.lives -= 1
                lives = self.ids['lives']
                lives.text = f"lives : {str(self.lives)}"
            else:
                label = self.ids['status']
                label.text = "GAME OVER"

        # bounce off left and right
        if (self.ball.x < 0) or (self.ball.x > self.width):
            self.ball.velocity_x *= -1
        for brick in self.brick_list:
            self.destroy_brick(self.ball, brick)

        self.pad.bounce_ball(self.ball)

        if len(self.brick_list) == 0:
            label = self.ids['status']
            label.text = 'SUIIIIIIIIIIII!!!'

    def serve_ball(self, vel=(0, -4)):
        self.ball.pos = (400, 200)
        self.ball.velocity = vel


class BreakOut_app(App):
    def build(self):
        self.width = Window.width
        self.height = Window.height
        game = Game()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == "__main__":
    BreakOut_app().run()
