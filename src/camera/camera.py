"""
@file camera.py
@brief This file contains the camera class.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from core.constants.settings import (
    ASPECT_RATIO,
    FAR,
    FOV_DEG,
    H_FOV,
    NEAR,
    PITCH_MAX,
    PLAYER_POSITION,
    V_FOV,
)

# Libraries
import glm


class Camera:
    def __init__(self, position, yaw, pitch) -> None:
        """
        Initialize the camera.
        :param: position: glm.vec3
        :param: yaw: float
        :param: pitch: float
        """
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.forward = glm.vec3(0.0, 0.0, -1.0)

        self.m_projection = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.m_view = glm.mat4()

    def update(self) -> None:
        """
        Update the camera.
        """
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self) -> None:
        """
        Update the view matrix.
        """
        self.m_view = glm.lookAt(self.position, self.position + self.forward, self.up)

    def update_vectors(self) -> None:
        """
        Update the camera vectors.
        """
        self.forward.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.forward.y = glm.sin(self.pitch)
        self.forward.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0.0, 1.0, 0.0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def rotate_pitch(self, delta_y) -> None:
        """
        Rotate the camera pitch.
        :param: delta_y: float
        """
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x) -> None:
        """
        Rotate the camera yaw.
        :param: delta_x: float
        """
        self.yaw -= delta_x

    def move_left(self, velocity) -> None:
        """
        Move the camera left.
        :param: velocity: float
        """
        self.position -= self.right * velocity

    def move_right(self, velocity) -> None:
        """
        Move the camera right.
        :param: velocity: float
        """
        self.position += self.right * velocity

    def move_up(self, velocity) -> None:
        """
        Move the camera up.
        :param: velocity: float
        """
        self.position += self.up * velocity

    def move_down(self, velocity) -> None:
        """
        Move the camera down.
        :param: velocity: float
        """
        self.position -= self.up * velocity

    def move_forward(self, velocity) -> None:
        """
        Move the camera forward.
        :param: velocity: float
        """
        self.position += self.forward * velocity

    def move_backward(self, velocity) -> None:
        """
        Move the camera backward.
        :param: velocity: float
        """
        self.position -= self.forward * velocity
