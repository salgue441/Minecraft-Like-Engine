"""
@file cube_marker.py
@brief Cube marker class for the game. 
@author Carlos Salguero
@version 1.0
@date 2023-07-10
"""

# Imports
import glm

# Project files
from graphics.meshes.block_mesh import BlockMesh


class BlockMarker:
    def __init__(self, block_handler) -> None:
        """
        Initializes the CubeMarker class.
        :param block_handler: The block handler to be used.
        """
        self.app = block_handler.app
        self.handler = block_handler
        self.position = glm.vec3(0)
        self.m_model = self.get_model_matrix()
        self.mesh = BlockMesh(self.app)

    def update(self) -> None:
        """
        Updates the cube marker.
        """
        if self.handler.block_id:
            if self.handler.interaction_mode:
                self.position = (
                    self.handler.block_world_position + self.handler.block_normal
                )

            else:
                self.position = self.handler.block_world_position

    def set_uniform(self) -> None:
        """
        Sets the uniform for the cube marker.
        """
        self.mesh.program["mode_id"] = self.handler.interaction_mode
        self.mesh.program["m_model"].write(self.get_model_matrix())

    def get_model_matrix(self) -> glm.mat4:
        """
        Gets the model matrix for the cube marker.
        :return: The model matrix for the cube marker.
        """
        return glm.translate(
            glm.mat4(1.0), glm.vec3(self.position.x, self.position.y, self.position.z)
        )

    def render(self) -> None:
        """
        Renders the cube marker.
        """
        if self.handler.block_id:
            self.set_uniform()
            self.mesh.render()
