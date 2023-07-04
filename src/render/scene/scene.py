"""
@file scene.py
@brief Renderes a scene of the game
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

from render.meshes.quad_mesh import QuadMesh
from render.world_objects.chunk import Chunk


class Scene:
    def __init__(self, app) -> None:
        """
        Initializes the scene.
        :param app: The main application
        """
        self.app = app
        self.chunk = Chunk(self.app)

    def update(self) -> None:
        pass

    def render(self) -> None:
        """
        Renders the scene.
        """
        self.chunk.render()
