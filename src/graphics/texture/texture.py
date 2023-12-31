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

        # Texture loading
        self.texture_0 = self.load("frame.png")
        self.texture_array_0 = self.load("atlas.png", is_tex_array=True)

        # Texture usage
        self.texture_0.use(location=0)
        self.texture_array_0.use(location=1)

    def load(self, file_name, is_tex_array=False) -> mg.Texture:
        """
        Loads the texture
        :param file_name: The name of the texture file
        :return: The texture
        """
        image = pg.image.load(f"assets/textures/{file_name}")
        image = pg.transform.flip(image, flip_x=True, flip_y=False)
        image_width, image_height = image.get_size()

        if is_tex_array:
            num_layers = 3 * image_height // image_width
            image = self.app.ctx.texture_array(
                size=(image_width, image_height // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(image, "RGBA"),
            )

        else:
            image = self.ctx.texture(
                size=(image_width, image_height),
                components=4,
                data=pg.image.tostring(image, "RGBA", False),
            )

        image.anisotropy = 32.0
        image.build_mipmaps()
        image.filter = (mg.NEAREST, mg.NEAREST)

        return image
