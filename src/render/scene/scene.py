"""
@file scene.py
@brief Renderes a scene of the game
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

from graphics.meshes.quad_mesh import QuadMesh
from render.world.world import World


class Scene:
    def __init__(self, app) -> None:
        """
        Initializes the scene.
        :param app: The main application
        """
        self.app = app
        self.chunk = World(self.app)

    def update(self) -> None:
        """
        Updates the scene.
        """
        self.chunk.update()

    def render(self) -> None:
        """
        Renders the scene.
        """
        self.chunk.render()
