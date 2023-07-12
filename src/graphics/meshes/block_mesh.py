"""
@file cube_mesh.py
@brief Creates a cube mesh for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-10
"""

# Imports
import numpy as np

# Project files
from graphics.meshes.base_mesh import BaseMesh


class BlockMesh(BaseMesh):
    def __init__(self, app) -> None:
        """
        Initializes the CubeMesh class.
        :param app: The application to be used.
        """
        self.app = app
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.block_marker
        self.vbo_format = "2f2 3f2"
        self.attributes = ("in_text_coord_0", "in_position")
        self.vao = self.get_vao()

    @staticmethod
    def get_data(vertices, indices) -> np.array:
        """
        Gets the data for the mesh.
        :param vertices: The vertices of the mesh.
        :param indices: The indices of the mesh.
        :return: The data for the mesh.
        """
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype=np.float16)

    def get_vertex_data(self) -> np.hstack:
        """
        Gets the vertex data for the mesh.
        :return: The vertex data for the mesh.
        """
        vertices = [
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (0, 1, 1),
            (0, 1, 0),
            (0, 0, 0),
            (1, 0, 0),
            (1, 1, 0),
        ]

        indices = [
            (0, 2, 3),
            (0, 1, 2),
            (1, 7, 2),
            (1, 6, 7),
            (6, 5, 4),
            (4, 7, 6),
            (3, 4, 5),
            (3, 5, 0),
            (3, 7, 4),
            (3, 2, 7),
            (0, 6, 1),
            (0, 5, 6),
        ]

        vertex_data = self.get_data(vertices, indices)
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [
            (0, 2, 3),
            (0, 1, 2),
            (0, 2, 3),
            (0, 1, 2),
            (0, 1, 2),
            (2, 3, 0),
            (2, 3, 0),
            (2, 0, 1),
            (0, 2, 3),
            (0, 1, 2),
            (3, 1, 2),
            (3, 0, 1),
        ]

        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)
        vertex_data = np.hstack((tex_coord_data, vertex_data))

        return vertex_data
