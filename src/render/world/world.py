"""
@file world.py
@brief World class for rendering the world
@author Carlos Salguero
@version 1.0
@date 2023-07-06
"""

import numpy as np

from core.constants.settings import (
    WORLD_VOLUME,
    CHUNK_VOLUME,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    WORLD_DEPTH,
    WORLD_AREA,
)

from render.world_objects.chunk import Chunk


class World:
    def __init__(self, app) -> None:
        """
        Initializes the world class
        """
        self.app = app
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        self.blocks = np.empty([WORLD_VOLUME, CHUNK_VOLUME], dtype=np.uint8)
        self.build_chunks()
        self.build_chunk_mesh()

    def build_chunks(self) -> None:
        """
        Builds the chunks in the world
        """
        for x in range(WORLD_WIDTH):
            for y in range(WORLD_HEIGHT):
                for z in range(WORLD_DEPTH):
                    chunk = Chunk(self, position=(x, y, z))
                    chunk_index = x + WORLD_WIDTH * z + WORLD_AREA * y
                    self.chunks[chunk_index] = chunk

                    # Chunk blocks
                    self.blocks[chunk_index] = chunk.build_blocks()
                    chunk.blocks = self.blocks[chunk_index]

    def build_chunk_mesh(self) -> None:
        """
        Builds the mesh for each chunk
        """
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self) -> None:
        """
        Updates the world
        """
        pass

    def render(self) -> None:
        """
        Renders the world
        """
        for chunk in self.chunks:
            chunk.render()
