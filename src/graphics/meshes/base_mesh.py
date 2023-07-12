"""
@file base_mesh.py
@brief Contains the base mesh class. 
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""
import numpy as np


class BaseMesh:
    def __init__(self) -> None:
        """
        Initializes the base mesh.
        """
        self.ctx = None
        self.program = None
        self.vbo_format = None
        self.attributes: tuple[str, ...] = None
        self.vao = None

    def get_vao(self) -> np.array:
        """
        Gets the vertex array object.
        :return: The vertex array object
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        vao = self.ctx.vertex_array(
            self.program, [(vbo, self.vbo_format, *self.attributes)], skip_errors=True
        )

        return vao

    def get_vertex_data(self) -> np.array:
        ...

    def render(self) -> None:
        """
        Renders the mesh.
        """
        self.vao.render()
