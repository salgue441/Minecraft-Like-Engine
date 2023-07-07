"""
@file chunk_mesh.py
@brief Contains the chunk mesh class for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from graphics.meshes.base_mesh import BaseMesh
from graphics.meshes.chunk_mesh_builder import build_chunk_mesh

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

        self.vbo_format = "3u1 1u1 1u1"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attributes = ("in_position", "voxel_id", "face_id")
        self.vao = self.get_vao()

    def get_vertex_data(self) -> np.array:
        mesh = build_chunk_mesh(
            chunk_voxels=self.chunk.voxels,
            format_size=self.format_size,
            chunk_pos=self.chunk.position,
            world_voxels=self.chunk.world.voxels,
        )

        return mesh
