"""
@file block_handler.py
@brief Handler for the block data.
@author Carlos Salguero
@version 1.0
@date 2023-07-10
"""

# Imports
import glm

# Project files
from core.constants.settings import (
    MAX_RAY_DISTANCE,
    CHUNK_SIZE,
    CHUNK_AREA,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    WORLD_DEPTH,
    WORLD_AREA,
)

from utils.chunk_builder.chunk_mesh_builder import get_chunk_index


class BlockHandler:
    def __init__(self, world) -> None:
        """
        Initializes the BlockHandler class.
        :param world: The world to be handled.
        """
        self.app = world.app
        self.chunks = world.chunks

        # Raycast
        self.chunk = None
        self.block_id = None
        self.block_index = None
        self.block_local_position = None
        self.block_world_position = None
        self.block_normal = None

        self.interaction_mode = 0
        self.new_block_id = 1

    def get_block_id(self, position) -> tuple:
        """
        Gets the block id at the given position.
        :param position: The position to get the block id from.
        :return: The block id at the given position. If the position is out of bounds, returns 0.
        """
        cx, cy, cz = chunk_position = position / CHUNK_SIZE

        if 0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH:
            chunk_index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
            chunk = self.chunks[chunk_index]

            lx, ly, lz = position = position - chunk_position * CHUNK_SIZE

            block_index = lx + CHUNK_SIZE * lz + CHUNK_AREA * ly
            block_id = chunk.blocks[block_index]

            return block_id, block_index, position, chunk

        return 0, 0, 0, 0

    def add_block(self) -> None:
        """
        Adds a voxel to the world.
        """
        if self.block_id:
            result = self.get_block_id(self.block_world_position + self.block_normal)

            if not result[0]:
                _, block_index, _, chunk = result
                chunk.blocks[block_index] = self.new_block_id
                chunk.mesh.rebuild()

                if chunk.is_empty:
                    chunk.is_empty = False

    def set_block(self) -> None:
        """
        Sets a voxel to the world.
        """
        if self.interaction_mode:
            self.add_block()

        else:
            self.remove_block()

    def switch_mode(self) -> None:
        """
        Switches the interaction mode. 0 is remove, 1 is add.
        """
        self.interaction_mode = not self.interaction_mode

    def remove_block(self) -> None:
        """
        Removes a voxel from the world.
        """
        if self.block_id:
            self.chunk.blocks[self.block_index] = 0

            self.chunk.mesh.rebuild()
            self.rebuild_adjacent_chunks()

    def rebuild_adjacent_chunks(self) -> None:
        """
        Rebuilds the adjacent chunks.
        """
        lx, ly, lz = self.block_local_position
        wx, wy, wz = self.block_world_position

        if lx == 0:
            self.rebuild_adjacent_chunk((wx - 1, wy, wz))

        elif lx == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx + 1, wy, wz))

        if ly == 0:
            self.rebuild_adjacent_chunk((wx, wy - 1, wz))

        elif ly == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy + 1, wz))

        if lz == 0:
            self.rebuild_adjacent_chunk((wx, wy, wz - 1))

        elif lz == CHUNK_SIZE - 1:
            self.rebuild_adjacent_chunk((wx, wy, wz + 1))

    def rebuild_adjacent_chunk(self, position) -> None:
        """
        Rebuilds the adjacent chunk at the given position.
        :param position: The position of the adjacent chunk to rebuild.
        """
        index = get_chunk_index(position)

        if index != -1:
            self.chunks[index].mesh.rebuild()

    def raycast(self) -> bool:
        """
        Raycasts from the camera to the world.
        :return: True if the raycast hit a block, False otherwise.
        """

        # Start and end positions
        x1, y1, z1 = self.app.player.position
        x2, y2, z2 = (
            self.app.player.position + self.app.player.forward * MAX_RAY_DISTANCE
        )

        # Current position
        current_block_position = glm.ivec3(x1, y1, z1)
        self.block_id = 0
        self.block_normal = glm.ivec3(0)
        step_direction = -1

        # Ray direction
        dx = glm.sign(x2 - x1)
        delta_x = min(dx / (x2 - x1), 10000000.0) if dx != 0 else 10000000.0
        max_x = delta_x * (1.0 - glm.fract(x1)) if dx > 0 else delta_x * glm.fract(x1)

        dy = glm.sign(y2 - y1)
        delta_y = min(dy / (y2 - y1), 10000000.0) if dy != 0 else 10000000.0
        max_y = delta_y * (1.0 - glm.fract(y1)) if dy > 0 else delta_y * glm.fract(y1)

        dz = glm.sign(z2 - z1)
        delta_z = min(dz / (z2 - z1), 10000000.0) if dz != 0 else 10000000.0
        max_z = delta_z * (1.0 - glm.fract(z1)) if dz > 0 else delta_z * glm.fract(z1)

        while not (max_x > 1.0 and max_y > 1.0 and max_z > 1.0):
            result = self.get_block_id(current_block_position)

            if result[0]:
                (
                    self.block_id,
                    self.block_index,
                    self.block_local_position,
                    self.chunk,
                ) = result

                self.block_world_position = current_block_position

                if step_direction == 0:
                    self.block_normal.x = -dx

                elif step_direction == 1:
                    self.block_normal.y = -dy

                else:
                    self.block_normal.z = -dz

                return True

            if max_x < max_y:
                if max_x < max_z:
                    current_block_position.x += dx
                    max_x += delta_x
                    step_direction = 0

                else:
                    current_block_position.z += dz
                    max_z += delta_z
                    step_direction = 2

            else:
                if max_y < max_z:
                    current_block_position.y += dy
                    max_y += delta_y
                    step_direction = 1

                else:
                    current_block_position.z += dz
                    max_z += delta_z
                    step_direction = 2

        return False

    def update(self) -> None:
        """
        Updates the world.
        """
        self.raycast()
