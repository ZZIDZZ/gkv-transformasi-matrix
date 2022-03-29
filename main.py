from manim import *

class Transformasi(ThreeDScene):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.move_camera(phi=45*DEGREES, theta=45*DEGREES, focal_distance=5)
        axis = ThreeDAxes()
        self.play(FadeIn(axis))
        dode = Dodecahedron()
        dode.set_stroke(BLUE_B, opacity=1.0)
        dode.set_fill(BLUE_B, opacity=1.0)

        self.play(DrawBorderThenFill(dode))
        self.play(dode.animate.shift(RIGHT))
        self.play(Rotate(dode, angle=PI/3, about_point=ORIGIN, rate_func=smooth))
        self.play(dode.animate.shift(RIGHT))

        self.wait()