"""
@file player.py
@brief This file contains the player class.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Libraries
import pygame as pg

# Project files
from camera.camera import Camera
from core.constants.settings import (
    PLAYER_POSITION,
    PLAYER_SPEED,
    PITCH_MAX,
    MOUSE_SENSITIVITY,
)


class Player(Camera):
    def __init__(self, app, position=PLAYER_POSITION, yaw=-90, pitch=0) -> None:
        """
        Initialize the player.
        :param: app: App
        :param: position: glm.vec3
        :param: yaw: float
        :param: pitch: float
        """
        self.app = app
        super().__init__(position, yaw, pitch)

    def update(self) -> None:
        """
        Update the player.
        """
        self.mouse_control()
        self.keyboard_control()
        super().update()

    def keyboard_control(self) -> None:
        """
        Control the player with the keyboard.
        """
        key_state = pg.key.get_pressed()
        velocity = PLAYER_SPEED * self.app.delta_time

        if key_state[pg.K_w]:
            self.move_forward(velocity)

        if key_state[pg.K_s]:
            self.move_backward(velocity)

        if key_state[pg.K_a]:
            self.move_left(velocity)

        if key_state[pg.K_d]:
            self.move_right(velocity)

    def mouse_control(self) -> None:
        """
        Control the player with the mouse.
        """
        mouse_delta = pg.mouse.get_rel()
        mouse_delta = (
            mouse_delta[0] * self.app.delta_time,
            mouse_delta[1] * self.app.delta_time,
        )

        self.yaw += mouse_delta[0] * MOUSE_SENSITIVITY
        self.pitch += mouse_delta[1] * MOUSE_SENSITIVITY

        self.pitch = max(min(self.pitch, PITCH_MAX), -PITCH_MAX)
