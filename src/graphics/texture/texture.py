"""
@file texture.py
@brief Contains the texture class for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-06
"""

import pygame as pg
import moderngl as mg


class Texture:
    def __init__(self, app) -> None:
        """
        Initializes the class
        :param: app The main application
        """
        self.app = app
        self.ctx = app.ctx

        self.texture_0 = self.load("frame.png")
        self.texture_0.use(location=0)

    def load(self, file_name) -> mg.Texture:
        """
        Loads the texture
        :param file_name: The name of the texture file
        :return: The texture
        """
        image = pg.image.load(f"assets/textures/{file_name}")
        image = pg.transform.flip(image, flip_x=True, flip_y=False)
        image_width, image_height = image.get_size()

        texture = self.ctx.texture(
            size=(image_width, image_height),
            components=4,
            data=pg.image.tostring(image, "RGBA", False),
        )

        texture.antisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mg.LINEAR_MIPMAP_LINEAR, mg.LINEAR)

        return texture
