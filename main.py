from typing import List
from manim import *
import numpy as np

np.set_printoptions(threshold=np.inf)

class Transformasiabrrot(ThreeDScene, MovingCamera):
    def __init__(self):
        super().__init__()

    def construct(self):
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=15)

        self.construct_axis()
        # self.setup_cube()
        self.setup_polyhedra()
        self.write_mat()
        self.do_translate(2, 3, 2)
        self.do_scale(2)
        self.do_rotation(90)
        self.do_abrrot([2, 1, 0], [3, 3, 1], 5)


    def construct_axis(self):
        axis = ThreeDAxes()
        axis.set_z_index(3)
        labz = axis.get_z_axis_label(Tex("$z$"))
        laby = axis.get_y_axis_label(Tex("$y$"))
        labx = axis.get_x_axis_label(Tex("$x$"))

        self.play(FadeIn(axis), Write(labz), Write(laby), Write(labx))

    def setup_cube(self):
        self.main_obj = main_obj = Cube(side_length=1)
        main_obj.shift(RIGHT + 2*UP)
        main_obj.set_stroke(BLUE_B, opacity=1.0)
        main_obj.set_fill(BLUE_B, opacity=1.0)

        self.play(DrawBorderThenFill(main_obj))

        self.wait(0.5)

    def setup_polyhedra(self):
        # som som major
        poly_points = [
            [ 1, 0, 0], # V0 kanan
            [ 0, 1, 0], # V1 atas
            [-1, 0, 0], # V2 kiri
            [ 0,-1, 0], # V3 bawah
            [ 0, 0, 1], # V4 keluar
            [ 0, 0,-1]  # V5 crot
        ]
        faces_list = [
            [0, 1, 4],
            [0, 1, 5],
            [1, 2, 4],
            [1, 2, 5],
            [2, 3, 4],
            [2, 3, 5],
            [3, 0, 4],
            [3, 0, 5],
        ]
        self.main_obj = main_obj = Polyhedron(vertex_coords=poly_points, faces_list=faces_list)
        self.play(DrawBorderThenFill(main_obj))
        self.move_camera(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=15, frame_center=main_obj.get_center())
        # self.play(main_obj.animate.shift(2*RIGHT + 2*UP))
        self.wait(0.5)

    def write_mat(self):
        def get_cu_vertices():
            points = self.main_obj.get_all_points()
            points = points.round(2)
            new_array = [tuple(row) for row in points]
            vertices = np.unique(new_array, axis=0)

            vertices = vertices[[0, 3, 8, 11, 20, 23, 28, 31], :]
            vertices = vertices.transpose()
            vertices = np.append(vertices, [[1, 1, 1, 1, 1, 1, 1, 1]], axis=0)
            return vertices

        def get_poly_coords():
            coords_faces = self.main_obj.extract_face_coords()
            # [print(n, n.shape) for n in coords_faces[0] + coords_faces[5]]
            coords = np.stack(coords_faces[0] + coords_faces[5])
            coords = coords.round(2)
            print(coords)
            coords = coords.transpose()
            coords = np.append(coords, [[1, 1, 1, 1, 1, 1]], axis=0)
            print(coords)
            return coords

        def matrix_updater(mob:Matrix):
            # https://www.reddit.com/r/manim/comments/oid6hv/comment/h4vxk5y/?utm_source=share&utm_medium=web2x&context=3
            newMat = Matrix(get_poly_coords(), h_buff=2)
            newMat.scale(0.5)
            newMat.to_corner(UP + RIGHT)
            newMat.shift(OUT*20)
            mob.become(newMat, copy_submobjects=False)

        pmat = Matrix(get_poly_coords(), h_buff=2)
        self.add_fixed_in_frame_mobjects(pmat)
        pmat.scale(0.5)
        pmat.to_corner(UP + RIGHT)

        self.play(Write(pmat))
        # self.add(pmat)
        self.wait()
        pmat.add_updater(matrix_updater)
    
    def do_abrrot(self, startp, endp, dur):

        def main_obj_rot_updater(main_obj_r, dt):
            main_obj_r.rotate(angle=dt, axis=AB, about_point=point_rot)

        # https://gamedev.stackexchange.com/questions/72528/how-can-i-project-a-3d-point-onto-a-3d-line
        self.rot_axis = rot_axis = Line3D(startp, endp)
        AB = rot_axis.end - rot_axis.start
        AP = self.main_obj.get_center() - rot_axis.start
        point_rot = rot_axis.start + np.dot(AP, AB) / np.dot(AB, AB) * AB

        self.play(Write(rot_axis))
        # self.add(rot_axis)

        self.move_camera(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=20, frame_center=rot_axis.get_center())
        self.begin_ambient_camera_rotation(45*DEGREES/3, about='theta')
        self.main_obj.add_updater(main_obj_rot_updater)
        self.wait(dur)
        # self.stop_ambient_camera_rotation(about='theta')


        # self.play(self.main_obj.rotate(angle=360*DEGREES, axis=AB, about_point=point_rot))
    
    def do_translate(self, x, y, z):
        self.play(self.main_obj.animate.shift(x*RIGHT + y*UP + z*OUT))
        self.move_camera(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=15, frame_center=self.main_obj.get_center())

    def do_scale(self, scale_fact):
        self.play(self.main_obj.animate.scale(scale_fact))
        self.move_camera(phi=60*DEGREES, theta=-45*DEGREES, focal_distance=15, frame_center=self.main_obj.get_center())

    def do_rotation(self, deg):
        self.play(self.main_obj.animate.rotate(angle=deg*DEGREES, axis=OUT, about_point=ORIGIN))
