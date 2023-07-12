"""
@file frustum.py
@brief Frustum class for the game. 
@author Carlos Salguero
@version 1.0
@date 2023-07-10
"""

# Imports
import glm
import math

# Project files
from core.constants.settings import CHUNK_SPHERE_RADIUS, V_FOV, H_FOV, NEAR, FAR


class Frustum:
    def __init__(self, camera) -> None:
        """
        Initializes the Frustum class.
        :param camera: The camera to be used.
        """
        self.camera = camera

        # Frustum planes
        self.factor_y = 1.0 / math.cos(half_y := V_FOV / 2.0)
        self.tan_y = math.tan(half_y)

        self.factor_x = 1.0 / math.cos(half_x := H_FOV / 2.0)
        self.tan_x = math.tan(half_x)

    def is_on_frustum(self, chunk) -> bool:
        """
        Checks if the given chunk is on the frustum.
        :param chunk: The chunk to be checked.
        :return: True if the chunk is on the frustum
        :return: False if the chunk is not on the frustum
        """
        sphere_vector = chunk.center - self.camera.position

        # Outside the Near and Far planes
        sphere_z = glm.dot(sphere_vector, self.camera.forward)

        if not (NEAR - CHUNK_SPHERE_RADIUS < sphere_z < FAR + CHUNK_SPHERE_RADIUS):
            return False

        # Outside the Left and Right planes
        sphere_x = glm.dot(sphere_vector, self.camera.right)
        distance = self.factor_x * CHUNK_SPHERE_RADIUS + sphere_z * self.tan_x

        if not (-distance <= sphere_x <= distance):
            return False

        # Outside the Top and Bottom planes
        sphere_y = glm.dot(sphere_vector, self.camera.up)
        distance = self.factor_y * CHUNK_SPHERE_RADIUS + sphere_z * self.tan_y

        if not (-distance <= sphere_y <= distance):
            return False

        return True
