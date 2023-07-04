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

# Colors
BG_COLOR = glm.vec3(0.1, 0.16, 0.25)

# Paths
SHADERS_PATH = "render/shaders"

# Camera
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 45.0
V_FOV = glm.radians(FOV_DEG)
H_FOV = 2.0 * glm.atan(glm.tan(V_FOV / 2.0) * ASPECT_RATIO)
NEAR = 0.1
FAR = 2000.0
PITCH_MAX = glm.radians(89.0)

# Player
PLAYER_SPEED = 0.1
PLAYER_ROTATION_SPEED = 0.1
PLAYER_POSITION = glm.vec3(0.0, 0.0, 1.0)

MOUSE_SENSITIVITY = 0.1
