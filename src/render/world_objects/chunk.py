"""
@file chunk.py
@brief Contains the chunk class for the game. 
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from core.constants.settings import CHUNK_VOLUME, CHUNK_SIZE, CHUNK_AREA
from render.meshes.chunk_mesh import ChunkMesh

# Libraries
import numpy as np
import glm


class Chunk:
    def __init__(self, app) -> None:
        """
        Initializes the chunk
        :param app: The main application
        """
        self.app = app
        self.voxels: np.array = self.build_voxels()
        self.mesh: ChunkMesh = None
        self.build_mesh()

    def build_voxels(self) -> np.array:
        """
        Builds the voxels of the chunk
        :return: The voxels of the chunk
        """
        voxels = np.zeros(CHUNK_VOLUME, dtype="uint8")

        # fill chunk
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                for y in range(CHUNK_SIZE):
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = (
                        x + y + z
                        if int(glm.simplex(glm.vec3(x, y, z) * 0.1) + 1)
                        else 0
                    )

        return voxels

    def build_mesh(self) -> None:
        """
        Builds the mesh of the chunk
        """
        self.mesh = ChunkMesh(self)

    def render(self) -> None:
        """
        Renders the chunk
        """
        self.mesh.render()
