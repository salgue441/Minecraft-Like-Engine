"""
@file chunk_mesh.py
@brief Contains the chunk mesh class for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from graphics.meshes.base_mesh import BaseMesh
from utils.chunk_builder.chunk_mesh_builder import build_chunk_mesh

# Libraries
import numpy as np


class ChunkMesh(BaseMesh):
    def __init__(self, chunk) -> None:
        """
        Initializes the chunk mesh
        :param chunk: The chunk
        """
        super().__init__()
        self.app = chunk.app
        self.chunk = chunk
        self.ctx = self.app.ctx
        self.program = self.app.shader_program.chunk

        self.vbo_format = "1u4"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attributes = ("packed_data",)
        self.vao = self.get_vao()

    def rebuild(self) -> None:
        """
        Rebuilds the chunk mesh.
        """
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        """
        Gets the vertex data.
        :return: The vertex data
        """

        return build_chunk_mesh(
            chunk_blocks=self.chunk.blocks,
            format_size=self.format_size,
            chunk_position=self.chunk.position,
            world_blocks=self.chunk.world.blocks,
        )
