"""
@file chunk_mesh_builder.py
@brief Auxiliar functions for building the chunk mesh of the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from core.constants.settings import (
    CHUNK_VOLUME,
    CHUNK_SIZE,
    CHUNK_AREA,
    WORLD_WIDTH,
    WORLD_HEIGHT,
    WORLD_DEPTH,
    WORLD_AREA,
)

# Libraries
import numpy as np
from numba import njit


@njit
def get_ao(local_position, world_position, world_blocks, plane) -> tuple:
    """
    Gets the ambient occlusion of the given block.
    :param local_position: The local position of the block.
    :param world_position: The world position of the block.
    :param world_blocks: The world blocks.
    :param plane: The plane to get the ambient occlusion from.
    :return: The ambient occlusion of the given block.
    :return: 0 If the block is not solid.
    """

    x, y, z = local_position
    wx, wy, wz = world_position

    if plane == "Y":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_blocks)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_blocks)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_blocks)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_blocks)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_blocks)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_blocks)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_blocks)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_blocks)

    elif plane == "X":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_blocks)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_blocks)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_blocks)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_blocks)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_blocks)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_blocks)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_blocks)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_blocks)

    else:
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_blocks)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_blocks)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_blocks)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_blocks)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_blocks)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_blocks)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_blocks)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_blocks)

    return ((a + b + c), (g + h + a), (e + f + g), (c + d + e))


@njit
def is_void(local_position, world_position, world_blocks) -> bool:
    """
    Checks if the given block is void.
    :param local_position: The local position of the block.
    :param world_position: The world position of the block.
    :param world_blocks: The world blocks.
    :return: True if the block is void.
    :return: False if the block is not void.
    """

    chunk_index = get_chunk_index(world_position)

    if chunk_index == -1:
        return False

    chunk_blocks = world_blocks[chunk_index]
    x, y, z = local_position
    block_index = (
        x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    )

    return not chunk_blocks[block_index]


@njit
def get_chunk_index(world_position) -> int:
    """
    Gets the chunk index of the given world position.
    :param world_position: The world position.
    :return: The chunk index.
    :return: -1 if the chunk index is out of bounds.
    """

    wx, wy, wz = world_position
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1

    index = cx + WORLD_WIDTH * cz + WORLD_AREA * cy
    return index


@njit
def pack_data(x, y, z, block_id, face_id, ao_id, flip_id) -> np.uint32:
    """
    Packs the given data into a single integer. The data is packed in the following order: 6 bits for the x position, 6 bits for the y position, 6 bits for the z position, 8 bits for the block id, 3 bits for the face id, 2 bits for the ao id and 1 bit for the flip id.
    :param x: The x position.
    :param y: The y position.
    :param z: The z position.
    :param block_id: The block id.
    :param face_id: The face id.
    :param ao_id: The ao id.
    :param flip_id: The flip id.
    :return: The packed data.
    """
    return (
        (x & 0x3F) << 26
        | (y & 0x3F) << 20
        | (z & 0x3F) << 14
        | (block_id & 0xFF) << 6
        | (face_id & 0x7) << 3
        | (ao_id & 0x3) << 1
        | (flip_id & 0x1)
    )


@njit
def add_data(vertex_data, index, *vertices) -> int:
    """
    Adds the given vertices to the vertex data.
    :param vertex_data: The vertex data.
    :param index: The index.
    :param vertices: The vertices.
    :return: The new index.
    """

    vertex_data[index : index + len(vertices)] = vertices
    return index + len(vertices)


@njit
def build_chunk_mesh(
    chunk_blocks, format_size, chunk_position, world_blocks
) -> np.array:
    """
    Builds the mesh for the given chunk.
    :param chunk_blocks: The chunk blocks.
    :param format_size: The format size.
    :param chunk_position: The chunk position.
    :param world_blocks: The world blocks.
    :return: The mesh.
    """
    vertex_data = np.empty(CHUNK_VOLUME * 18 * format_size, dtype="uint32")
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                block_id = chunk_blocks[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not block_id:
                    continue

                # Get the world position of the block.
                cx, cy, cz = chunk_position
                wx, wy, wz = (
                    cx * CHUNK_SIZE + x,
                    cy * CHUNK_SIZE + y,
                    cz * CHUNK_SIZE + z,
                )

                # Top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_blocks):
                    ao = get_ao(
                        (x, y + 1, z), (wx, wy + 1, wz), world_blocks, plane="Y"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y + 1, z, block_id, 0, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z, block_id, 0, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 0, ao[2], flip_id)
                    v3 = pack_data(x, y + 1, z + 1, block_id, 0, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)

                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # Bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_blocks):
                    ao = get_ao(
                        (x, y - 1, z), (wx, wy - 1, wz), world_blocks, plane="Y"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z, block_id, 1, ao[0], flip_id)
                    v1 = pack_data(x + 1, y, z, block_id, 1, ao[1], flip_id)
                    v2 = pack_data(x + 1, y, z + 1, block_id, 1, ao[2], flip_id)
                    v3 = pack_data(x, y, z + 1, block_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)

                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # Right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_blocks):
                    ao = get_ao(
                        (x + 1, y, z), (wx + 1, wy, wz), world_blocks, plane="X"
                    )
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x + 1, y, z, block_id, 2, ao[0], flip_id)
                    v1 = pack_data(x + 1, y + 1, z, block_id, 2, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 2, ao[2], flip_id)
                    v3 = pack_data(x + 1, y, z + 1, block_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)

                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # Left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_blocks):
                    ao = get_ao(
                        (x - 1, y, z), (wx - 1, wy, wz), world_blocks, plane="X"
                    )
                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z, block_id, 3, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z, block_id, 3, ao[1], flip_id)
                    v2 = pack_data(x, y + 1, z + 1, block_id, 3, ao[2], flip_id)
                    v3 = pack_data(x, y, z + 1, block_id, 3, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)

                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # Back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_blocks):
                    ao = get_ao(
                        (x, y, z - 1), (wx, wy, wz - 1), world_blocks, plane="Z"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z, block_id, 4, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z, block_id, 4, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z, block_id, 4, ao[2], flip_id)
                    v3 = pack_data(x + 1, y, z, block_id, 4, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)

                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                    # Front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_blocks):
                    ao = get_ao(
                        (x, y, z + 1), (wx, wy, wz + 1), world_blocks, plane="Z"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = pack_data(x, y, z + 1, block_id, 5, ao[0], flip_id)
                    v1 = pack_data(x, y + 1, z + 1, block_id, 5, ao[1], flip_id)
                    v2 = pack_data(x + 1, y + 1, z + 1, block_id, 5, ao[2], flip_id)
                    v3 = pack_data(x + 1, y, z + 1, block_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)
                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

    return vertex_data[: index + 1]
