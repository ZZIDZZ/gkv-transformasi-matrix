from manim import *
import numpy as np

class Transformasi(ThreeDScene, MovingCamera):
    def __init__(self):
        super().__init__()

    def construct(self):

        axis = ThreeDAxes()
        labz = axis.get_z_axis_label(Tex("$z$-label"))

        cu = Cube(side_length=1)
        cu.shift(RIGHT + 2*UP)
        cu.set_stroke(BLUE_B, opacity=1.0)
        cu.set_fill(BLUE_B, opacity=1.0)

        vertices = cu.get_all_points()

        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=10)

        self.play(FadeIn(axis), Write(labz))
        self.play(DrawBorderThenFill(cu))
        self.wait(0.5)

        # https://gamedev.stackexchange.com/questions/72528/how-can-i-project-a-3d-point-onto-a-3d-line
        rot_axis = Line3D([2, 1, 0], [3, 3, 1])
        self.play(Write(rot_axis))

        AB = rot_axis.end - rot_axis.start
        AP = cu.get_center() - rot_axis.start

        point_rot = rot_axis.start + np.dot(AP, AB) / np.dot(AB, AB) * AB
        self.begin_ambient_camera_rotation(45*DEGREES/3, about='theta')
        self.play(Rotate(cu, angle=10*360*DEGREES, axis=AB, about_point=point_rot, run_time=15, rate_func=linear))
    
        self.wait(5)
        self.stop_ambient_camera_rotation(about='theta')