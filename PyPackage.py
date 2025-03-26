import os
from time import time
import matplotlib.pyplot as plt
from sectionproperties.pre.library.primitive_sections import circular_section
from sectionproperties.pre.library.steel_sections import circular_hollow_section
from sectionproperties.analysis.section import Section
from sectionproperties.pre.geometry import Geometry
from shapely.geometry import Polygon


plt.switch_backend("Agg")  # 设置 matplotlib 使用 Agg 后端，这样就不会显示图形


class SectionProperty:
    def __init__(self, case_dir: str):
        self.__m_case_dir = case_dir
        self._m_geometry = None

    def calc_sect_prop(self):
        print()
        start = time()
        ax = self._m_geometry.plot_geometry()
        fig = ax.get_figure()
        fig.savefig(os.path.join(self.__m_case_dir, "Geometry.png"))
        plt.close(fig)

        section = Section(self._m_geometry)
        section.display_mesh_info()

        ax = section.plot_mesh(materials=False)
        fig = ax.get_figure()
        fig.savefig(os.path.join(self.__m_case_dir, "Mesh.png"))
        plt.close(fig)

        section.calculate_geometric_properties()
        section.calculate_warping_properties()
        section.display_results()

        ax = section.plot_centroids()
        fig = ax.get_figure()
        fig.savefig(os.path.join(self.__m_case_dir, "Centroids.png"))
        plt.close(fig)

        secpara = {
            "A": section.section_props.area,  # Cross-sectional area
            "IY": section.section_props.ixx_c,  # Second moment of area about the global x-axis
            "IYZ": section.section_props.ixy_c,  # Second moment of area about the centroidal xy-axis
            "IZ": section.section_props.iyy_c,  # Second moment of area about the global y-axis
            "JG": section.section_props.gamma,  # Warping constant
            "JX": section.section_props.j,  # Torsion constant
            "EY": section.section_props.cx,  # X coordinate of the elastic centroid
            "EZ": section.section_props.cy,  # Y coordinate of the elastic centroid
            # "SCY": section.section_props.x_se,  # Shear center Diff with Ansys  TODO don't change with translation
            # "SCZ": section.section_props.y_se,
            "AY": section.section_props.area / section.section_props.A_sx,  # Shear area about the x-axis
            "AZ": section.section_props.area / section.section_props.A_sy,  # Shear area about the y-axis
        }

        end = time()
        return end - start, secpara


class Circle(SectionProperty):
    def __init__(self, case_dir: str, radius: float):
        super().__init__(case_dir)

        d = radius * 2  # Diameter of the circle
        n = 64  # Number of points discretising the circle
        geometry = circular_section(d, n)
        self._m_geometry = geometry.create_mesh(mesh_sizes=[d / 25])  # generates a mesh with a maximum triangular area of 2.5


class Tube(SectionProperty):
    def __init__(self, case_dir: str, inner_radius: float, outer_radius: float):
        super().__init__(case_dir)

        d = outer_radius * 2  # Outer diameter of the CHS
        t = outer_radius - inner_radius  # Thickness of the CHS
        n = 64  # Number of points discretising the inner and outer circles
        geometry = circular_hollow_section(d, t, n)
        self._m_geometry = geometry.create_mesh(mesh_sizes=[min(d / 50, t / 3)])


class Rectangle(SectionProperty):
    def __init__(self, case_dir: str, width: float, height: float):
        super().__init__(case_dir)

        width_x = width / 2
        height_x = height / 2
        points = ((-width_x, -height_x), (width_x, -height_x), (width_x, height_x), (-width_x, height_x))  # Outer line
        geometry = Geometry(Polygon(points))
        self._m_geometry = geometry.create_mesh(mesh_sizes=[min(width, height) / 10])


class HollowRectangle(SectionProperty):
    def __init__(self, case_dir: str, width: float, height: float, left_thickness: float, right_thickness: float, bottom_thickness: float, top_thickness: float):
        super().__init__(case_dir)

        outer_points = ((0, 0), (width, 0), (width, height), (0, height))  # Outer line
        inner_points = ((left_thickness, bottom_thickness), (width - right_thickness, bottom_thickness), (width - right_thickness, height - top_thickness), (left_thickness, height - top_thickness))  # Inner line
        geometry = Geometry(Polygon(outer_points)) - Geometry(Polygon(inner_points))
        self._m_geometry = geometry.create_mesh(mesh_sizes=min(left_thickness, right_thickness, bottom_thickness, top_thickness) / 5)


class I(SectionProperty):
    def __init__(self, case_dir: str, bottom_width: float, top_width: float, height: float, bottom_flange_thickness: float, top_flange_thickness: float, web_thickness: float):
        super().__init__(case_dir)

        bot_flange_x = bottom_width / 2
        top_flange_x = top_width / 2
        web_x = web_thickness / 2
        points = ((-bot_flange_x, 0), (bot_flange_x, 0), (bot_flange_x, bottom_flange_thickness), (web_x, bottom_flange_thickness), (web_x, height - top_flange_thickness), (top_flange_x, height - top_flange_thickness), (top_flange_x, height), (-top_flange_x, height), (-top_flange_x, height - top_flange_thickness), (-web_x, height - top_flange_thickness), (-web_x, bottom_flange_thickness), (-bot_flange_x, bottom_flange_thickness))  # Outer line
        geometry = Geometry(Polygon(points))
        self._m_geometry = geometry.create_mesh(mesh_sizes=min(bottom_flange_thickness, top_flange_thickness, web_thickness) / 5)


class Chanel(SectionProperty):
    def __init__(self, case_dir: str, bottom_width: float, top_width: float, height: float, bottom_flange_thickness: float, top_flange_thickness: float, web_thickness: float):
        super().__init__(case_dir)

        points = ((0, 0), (bottom_width, 0), (bottom_width, bottom_flange_thickness), (web_thickness, bottom_flange_thickness), (web_thickness, height - top_flange_thickness), (top_width, height - top_flange_thickness), (top_width, height), (0, height))  # Outer line
        geometry = Geometry(Polygon(points))
        self._m_geometry = geometry.create_mesh(mesh_sizes=min(bottom_flange_thickness, top_flange_thickness, web_thickness) / 5)


class Tee(SectionProperty):
    def __init__(self, case_dir: str, width: float, height: float, flange_thickness: float, web_thickness: float):
        super().__init__(case_dir)

        width_x = width / 2
        web_x = web_thickness / 2
        flange_y = flange_thickness / 2
        points = ((width_x, 0), (width_x, flange_thickness), (web_x, flange_thickness), (web_x, height), (-web_x, height), (-web_x, flange_thickness), (-width_x, flange_thickness), (-width_x, 0))  # Outer line
        points2 = []
        for point in points:
            points2.append((point[0], point[1] - flange_y))
        geometry = Geometry(Polygon(points2))
        self._m_geometry = geometry.create_mesh(mesh_sizes=[min(flange_thickness, web_thickness) / 5])


class Angle(SectionProperty):
    def __init__(self, case_dir: str, width: float, height: float, bottom_leg_thickness: float, left_leg_thickness: float):
        super().__init__(case_dir)

        points = ((0, 0), (width, 0), (width, bottom_leg_thickness), (left_leg_thickness, bottom_leg_thickness), (left_leg_thickness, height), (0, height))  # Outer line
        trans_x, trans_y = left_leg_thickness / 2, bottom_leg_thickness / 2
        points2 = []
        for point in points:
            points2.append((point[0] - trans_x, point[1] - trans_y))
        geometry = Geometry(Polygon(points2))
        self._m_geometry = geometry.create_mesh(mesh_sizes=min(bottom_leg_thickness, left_leg_thickness) / 5)


class Custom(SectionProperty):
    def __init__(self, case_dir: str, outer_points: list, inner_points: list):
        super().__init__(case_dir)

        geometry = Geometry(Polygon(outer_points))
        if inner_points:
            geometry -= Geometry(Polygon(inner_points))
        self._m_geometry = geometry.create_mesh(mesh_sizes=100)

