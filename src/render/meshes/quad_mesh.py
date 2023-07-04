"""
@file quad_mesh.py
@brief Contains the quad mesh class. 
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""
import numpy as np
from render.meshes.base_mesh import BaseMesh


class QuadMesh(BaseMesh):
    def __init__(self, app):
        """
        Initializes the quad mesh.
        :param app: The main application
        """
        super().__init__()

        self.app = app
        self.ctx = app.ctx
        self.program = app.shader_program.quad

        # Format
        self.vbo_format = "3f 3f"
        self.attributes = ("in_position", "in_color")
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        """
        Gets the vertex data.
        :return: The vertex data
        """
        vertices = [
            (0.5, 0.5, 0.0),
            (-0.5, 0.5, 0.0),
            (-0.5, -0.5, 0.0),
            (0.5, 0.5, 0.0),
            (-0.5, -0.5, 0.0),
            (0.5, -0.5, 0.0),
        ]

        colors = [(0, 1, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (1, 1, 0), (0, 0, 1)]

        vertex_data = np.hstack([vertices, colors], dtype=np.float32)
        return vertex_data
