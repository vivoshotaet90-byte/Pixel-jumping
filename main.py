from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
import random

Window.clearcolor = (0.04, 0.06, 0.14, 1)

class Game(Widget):
    player_x = NumericProperty(70)
    player_y = NumericProperty(180)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.vx = 0
        self.vy = 0
        self.grounded = False
        self.score = 0
        self.world_speed = 3
        self.platforms = [(0, 100, 300), (350, 170, 150),
                          (570, 250, 180), (820, 160, 180),
                          (1080, 220, 200)]
        self.coins = [(400, 220), (620, 300), (900, 210), (1150, 270)]
        self.world_x = 0
        self.controls = set()
        self.status = Label(
            text="PIXEL JUMP     Монеты: 0",
            size_hint=(1, None), height=45,
            pos_hint={"top": 1}, bold=True
        )
        self.add_widget(self.status)
        Clock.schedule_interval(self.update, 1 / 60)

    def on_touch_down(self, touch):
        x = touch.x / max(self.width, 1)
        if x < 0.30:
            self.controls.add("left")
        elif x < 0.60:
            self.controls.add("right")
        else:
            self.controls.add("jump")
        return True

    def on_touch_up(self, touch):
        self.controls.discard("left")
        self.controls.discard("right")
        self.controls.discard("jump")
        return True

    def update(self, dt):
        dt = min(dt, 0.04)
        speed = 240
        self.vx = 0
        if "left" in self.controls:
            self.vx = -speed
        if "right" in self.controls:
            self.vx = speed
        if "jump" in self.controls and self.grounded:
            self.vy = 560
            self.grounded = False

        self.player_x += self.vx * dt
        self.vy -= 1250 * dt
        old_y = self.player_y
        self.player_y += self.vy * dt
        self.player_x = max(0, min(self.player_x, self.width - 38))

        self.grounded = False
        for px, py, pw in self.platforms:
            sx = px - self.world_x
            if (self.vy <= 0 and old_y >= py and
                self.player_y <= py and
                self.player_x + 32 > sx and
                self.player_x < sx + pw):
                self.player_y = py
                self.vy = 0
                self.grounded = True

        self.world_x += 100 * dt
        if self.world_x > 500:
            self.world_x = 0
            self.score += 1

        for coin in self.coins[:]:
            cx, cy = coin
            sx = cx - self.world_x
            if (abs(self.player_x + 16 - sx) < 28 and
                abs(self.player_y + 16 - cy) < 32):
                self.coins.remove(coin)
                self.score += 5

        if self.player_y < -50:
            self.player_x, self.player_y = 70, 180
            self.vy = 0
            self.world_x = 0

        self.status.text = f"PIXEL JUMP     Монеты: {self.score}"
        self.draw_scene()

    def draw_scene(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.04, 0.06, 0.14, 1)
            Rectangle(pos=(0, 0), size=self.size)

            Color(0.12, 0.18, 0.30, 1)
            for i in range(12):
                Rectangle(pos=(i * 90, 40), size=(35, 100 + (i % 3) * 35))

            for px, py, pw in self.platforms:
                sx = px - self.world_x
                if -pw < sx < self.width:
                    Color(0.15, 0.85, 0.55, 1)
                    Rectangle(pos=(sx, py - 12), size=(pw, 18))
                    Color(0.30, 0.45, 0.60, 1)
                    Rectangle(pos=(sx, py - 28), size=(pw, 16))

            for cx, cy in self.coins:
                sx = cx - self.world_x
                if -20 < sx < self.width + 20:
                    Color(1, 0.78, 0.12, 1)
                    Ellipse(pos=(sx, cy), size=(22, 22))

            Color(0.25, 0.65, 1, 1)
            Rectangle(pos=(self.player_x, self.player_y), size=(32, 38))
            Color(1, 1, 1, 1)
            Rectangle(pos=(self.player_x + 19, self.player_y + 23),
                      size=(5, 5))

            # Touch-control hints
            Color(1, 1, 1, 0.22)
            Ellipse(pos=(18, 18), size=(75, 75))
            Ellipse(pos=(105, 18), size=(75, 75))
            Ellipse(pos=(self.width - 95, 18), size=(75, 75))

            Color(1, 1, 1, 0.9)
            Rectangle(pos=(43, 52), size=(25, 5))
            Rectangle(pos=(53, 42), size=(5, 25))
            Rectangle(pos=(128, 52), size=(30, 5))
            Rectangle(pos=(self.width - 70, 48), size=(5, 30))
            Rectangle(pos=(self.width - 82, 60), size=(30, 5))

class PixelJumpApp(App):
    def build(self):
        return Game()

if __name__ == "__main__":
    PixelJumpApp().run()
