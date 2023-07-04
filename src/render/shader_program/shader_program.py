"""
@file shader_program.py
@brief Contains the shader program class for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""
from core.constants.settings import SHADERS_PATH
import moderngl as mg


class ShaderProgram:
    def __init__(self, app) -> None:
        """
        Initializes the shader program
        :param app: The main application
        """
        self.app = app
        self.ctx = app.ctx

        # Shaders
        self.quad = self.get_program(shader_name="quad")

        # Uniforms
        self.set_uniforms_on_init()

    def get_program(self, shader_name) -> mg.Program:
        """
        Gets the shader program
        :param shader_name: The name of the shader program
        :return: The shader program
        """
        with open(f"{SHADERS_PATH}/{shader_name}.vert", "r") as file:
            vertex_shader = file.read()

        with open(f"{SHADERS_PATH}/{shader_name}.frag", "r") as file:
            fragment_shader = file.read()

        return self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

    def set_uniforms_on_init(self) -> None:
        pass

    def update(self) -> None:
        pass
