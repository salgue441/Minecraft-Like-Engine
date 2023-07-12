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
from numba import uint8, njit


@njit
def get_ao(local_pos, world_pos, world_voxels, plane) -> float:
    """
    Gets the ambient occlusion of the given voxel position
    :param local_pos: The local voxel position
    :param world_pos: The world voxel position
    :param world_voxels: The world voxels
    :param plane: The plane to check
    :return: The ambient occlusion of the given voxel position
    """

    x, y, z = local_pos
    wx, wy, wz = world_pos

    if plane == "Y":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x - 1, y, z - 1), (wx - 1, wy, wz - 1), world_voxels)
        c = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        d = is_void((x - 1, y, z + 1), (wx - 1, wy, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x + 1, y, z + 1), (wx + 1, wy, wz + 1), world_voxels)
        g = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        h = is_void((x + 1, y, z - 1), (wx + 1, wy, wz - 1), world_voxels)

    elif plane == "X":
        a = is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels)
        b = is_void((x, y - 1, z - 1), (wx, wy - 1, wz - 1), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x, y - 1, z + 1), (wx, wy - 1, wz + 1), world_voxels)
        e = is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels)
        f = is_void((x, y + 1, z + 1), (wx, wy + 1, wz + 1), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x, y + 1, z - 1), (wx, wy + 1, wz - 1), world_voxels)

    else:
        a = is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels)
        b = is_void((x - 1, y - 1, z), (wx - 1, wy - 1, wz), world_voxels)
        c = is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels)
        d = is_void((x + 1, y - 1, z), (wx + 1, wy - 1, wz), world_voxels)
        e = is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels)
        f = is_void((x + 1, y + 1, z), (wx + 1, wy + 1, wz), world_voxels)
        g = is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels)
        h = is_void((x - 1, y + 1, z), (wx - 1, wy + 1, wz), world_voxels)

    return ((a + b + c), (g + h + a), (e + f + g), (c + d + e))


@njit
def to_uint8(x, y, z, voxel_id, face_id, ao_id, flip_id) -> uint8:
    """
    Converts the given parameters to a uint8
    :param x: The x coordinate
    :param y: The y coordinate
    :param z: The z coordinate
    :param voxel_id: The voxel id
    :param face_id: The face id
    :param ao_id: The ambient occlusion id
    :param flip_id: The flip id (0 or 1)
    :return: The uint8 value of the given parameters
    """
    return (
        uint8(x),
        uint8(y),
        uint8(z),
        uint8(voxel_id),
        uint8(face_id),
        uint8(ao_id),
        uint8(flip_id),
    )


@njit
def get_chunk_index(world_voxel_pos) -> int:
    """
    Gets the chunk index of the given voxel position
    :param world_voxel_pos: The world voxel position
    :return: The chunk index
    """
    wx, wy, wz = world_voxel_pos

    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    if not (0 <= cx < WORLD_WIDTH and 0 <= cy < WORLD_HEIGHT and 0 <= cz < WORLD_DEPTH):
        return -1

    return cx + WORLD_WIDTH * cz + WORLD_AREA * cy


@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels) -> bool:
    """
    Checks if the given voxel is void
    :param local_voxel_pos: The local voxel position
    :param world_voxel_pos: The world voxel position
    :param world_voxels: The world voxels
    :return: True if the voxel is void, False otherwise
    """

    chunk_index = get_chunk_index(world_voxel_pos)

    if chunk_index == -1:
        return False

    chunk_voxels = world_voxels[chunk_index]
    x, y, z = local_voxel_pos
    voxel_index = (
        x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA
    )

    if chunk_voxels[voxel_index]:
        return False

    return True


@njit
def add_data(vertex_data, index, *vertices) -> int:
    """
    Adds the given vertices to the vertex data
    :param vertex_data: The vertex data
    :param index: The index
    :param vertices: The vertices
    :return: The index
    """
    for vertex in vertices:
        for attribute in vertex:
            vertex_data[index] = attribute
            index += 1

    return index


@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels) -> np.array:
    """
    Builds the chunk mesh from the given chunk voxels. The chunk mesh is a numpy array of uint8 values.
    :param chunk_voxels: The chunk voxels
    :param format_size: The format size
    :param chunk_pos: The chunk position
    :param world_voxels: The world voxels
    :return: The chunk mesh
    """
    vertex_data = np.empty(CHUNK_VOLUME * 18 * format_size, dtype=np.uint8)
    index = 0

    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]

                if not voxel_id:
                    continue

                # World position
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE

                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    ao = get_ao(
                        (x, y + 1, z), (wx, wy + 1, wz), world_voxels, plane="Y"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y + 1, z, voxel_id, 0, ao[0], flip_id)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 0, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0, ao[2], flip_id)
                    v3 = to_uint8(x, y + 1, z + 1, voxel_id, 0, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v0, v3, v1, v3, v2)

                    else:
                        index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    ao = get_ao(
                        (x, y - 1, z), (wx, wy - 1, wz), world_voxels, plane="Y"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z, voxel_id, 1, ao[0], flip_id)
                    v1 = to_uint8(x + 1, y, z, voxel_id, 1, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1, ao[2], flip_id)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 1, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v1, v3, v0, v1, v2, v3)

                    else:
                        index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    ao = get_ao(
                        (x + 1, y, z), (wx + 1, wy, wz), world_voxels, plane="X"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x + 1, y, z, voxel_id, 2, ao[0], flip_id)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 2, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2, ao[2], flip_id)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 2, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)

                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    ao = get_ao(
                        (x - 1, y, z), (wx - 1, wy, wz), world_voxels, plane="X"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z, voxel_id, 3, ao[0], flip_id)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 3, ao[1], flip_id)
                    v2 = to_uint8(x, y + 1, z + 1, voxel_id, 3, ao[2], flip_id)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 3, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)

                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    ao = get_ao(
                        (x, y, z + 1), (wx, wy, wz + 1), world_voxels, plane="Z"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z + 1, voxel_id, 5, ao[0], flip_id)
                    v1 = to_uint8(x, y + 1, z + 1, voxel_id, 5, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5, ao[2], flip_id)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 5, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v1, v0, v3, v2, v1)

                    else:
                        index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    ao = get_ao(
                        (x, y, z - 1), (wx, wy, wz - 1), world_voxels, plane="Z"
                    )

                    flip_id = ao[1] + ao[3] > ao[0] + ao[2]

                    v0 = to_uint8(x, y, z, voxel_id, 4, ao[0], flip_id)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 4, ao[1], flip_id)
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4, ao[2], flip_id)
                    v3 = to_uint8(x + 1, y, z, voxel_id, 4, ao[3], flip_id)

                    if flip_id:
                        index = add_data(vertex_data, index, v3, v0, v1, v3, v1, v2)

                    else:
                        index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

    return vertex_data[: index + 1]
