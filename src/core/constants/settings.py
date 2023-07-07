"""
@file settings.py
@brief Contains all the settings for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

import glm

# Window properties
WIN_RES = glm.vec2(1600, 900)

# Chunk properties
CHUNK_SIZE = 32
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE * CHUNK_SIZE
CHUNK_VOLUME = CHUNK_AREA * CHUNK_SIZE

# Colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)

# Paths
SHADERS_PATH = "graphics/shaders"

# Camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 50
V_FOV = glm.radians(FOV_DEG)
H_FOV = 2.0 * glm.atan(glm.tan(V_FOV / 2.0) * ASPECT_RATIO)
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89.0)

# Player
PLAYER_SPEED = 0.05
PLAYER_ROTATION_SPEED = 0.04
PLAYER_POSITION = glm.vec3(H_CHUNK_SIZE, CHUNK_SIZE, 1.5 * CHUNK_SIZE)

MOUSE_SENSITIVITY = 0.002
