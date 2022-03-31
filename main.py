from manim import *
import numpy as np

class Transformasi(ThreeDScene, MovingCamera):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=10)

        self.construct_axis()
        self.setup_cube()
        self.write_mat()
        self.do_abrrot()


    def construct_axis(self):
        axis = ThreeDAxes()
        labz = axis.get_z_axis_label(Tex("$z$"))
        laby = axis.get_y_axis_label(Tex("$y$"))
        labx = axis.get_x_axis_label(Tex("$x$"))

        self.play(FadeIn(axis), Write(labz), Write(laby), Write(labx))

    def setup_cube(self):
        self.cu = cu = Cube(side_length=1)
        cu.shift(RIGHT + 2*UP)
        cu.set_stroke(BLUE_B, opacity=1.0)
        cu.set_fill(BLUE_B, opacity=1.0)

        self.play(DrawBorderThenFill(cu))
        self.wait(0.5)

    def write_mat(self):
        def get_cu_vertices():
            points = self.cu.get_all_points()
            points = points.round(2)
            new_array = [tuple(row) for row in points]
            vertices = np.unique(new_array, axis=0)
            vertices = vertices[[0, 3, 8, 11, 20, 23, 28, 31], :]
            vertices = vertices.transpose()
            return vertices

        def matrix_updater(mob:Matrix):
            # https://www.reddit.com/r/manim/comments/oid6hv/comment/h4vxk5y/?utm_source=share&utm_medium=web2x&context=3
            newMat = Matrix(get_cu_vertices())
            newMat.scale(0.5)
            newMat.to_corner(UP + LEFT)
            mob.become(newMat)

        pmat = Matrix(get_cu_vertices())
        pmat.add_updater(matrix_updater)
        self.add_fixed_in_frame_mobjects(pmat)
        pmat.scale(0.5)
        pmat.to_corner(UP + LEFT)

        self.play(Write(pmat))
        self.wait()
    
    def do_abrrot(self):

        def cu_rot_updater(cu_r, dt):
            cu_r.rotate(angle=dt, axis=AB, about_point=point_rot)

        # https://gamedev.stackexchange.com/questions/72528/how-can-i-project-a-3d-point-onto-a-3d-line
        self.rot_axis = rot_axis = Line3D([2, 1, 0], [3, 3, 1])
        AB = rot_axis.end - rot_axis.start
        AP = self.cu.get_center() - rot_axis.start
        point_rot = rot_axis.start + np.dot(AP, AB) / np.dot(AB, AB) * AB

        self.play(Write(rot_axis))
        self.begin_ambient_camera_rotation(45*DEGREES/3, about='theta')
        self.cu.add_updater(cu_rot_updater)
        # print(get_cu_vertices())
        # self.play(Rotating(self.cu, axis=AB, radians=180*DEGREES, about_point=point_rot))
        # print(get_cu_vertices())
        self.wait(20)
        # self.stop_ambient_camera_rotation(about='theta')


        # self.play(self.cu.rotate(angle=360*DEGREES, axis=AB, about_point=point_rot))