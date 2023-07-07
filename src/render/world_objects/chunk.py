"""
@file chunk.py
@brief Contains the chunk class for the game. 
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from core.constants.settings import CHUNK_VOLUME, CHUNK_SIZE, CHUNK_AREA
from graphics.meshes.chunk_mesh import ChunkMesh

# Libraries
import numpy as np
import glm


class Chunk:
    def __init__(self, world, position) -> None:
        """
        Initializes the class
        :param: world: The world
        :param: position: The position of the chunk
        """
        self.app = world.app
        self.world = world
        self.position = position
        self.m_model = self.get_model_matrix()
        self.voxels: np.array = None
        self.mesh: ChunkMesh = None
        self.is_empty = True

    def get_model_matrix(self) -> glm.mat4:
        """
        Gets the model matrix for the chunk
        :return: The model matrix
        """
        return glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)

    def set_uniform(self) -> None:
        """
        Sets the uniform for the chunk
        """
        self.mesh.program["m_model"].write(self.m_model)

    def build_mesh(self) -> None:
        """
        Builds the mesh for the chunk
        """
        self.mesh = ChunkMesh(self)

    def build_voxels(self) -> np.array:
        """
        Builds the voxels for the chunk
        """
        voxels = np.zeros(CHUNK_VOLUME, dtype=np.uint8)
        cx, cy, cz = glm.ivec3(self.position) * CHUNK_SIZE

        for x in range(CHUNK_SIZE):
            wx = x + cx

            for z in range(CHUNK_SIZE):
                wz = z + cz
                world_height = int(glm.simplex(glm.vec2(wx, wz) * 0.01) * 32 + 32)

                local_height = min(world_height - cy, CHUNK_SIZE)

                for y in range(local_height):
                    wy = y + cy
                    voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y] = wy + 1

        if np.any(voxels):
            self.is_empty = False

        return voxels

    def render(self) -> None:
        """
        Renders the chunk
        """
        if not self.is_empty:
            self.set_uniform()
            self.mesh.render()
