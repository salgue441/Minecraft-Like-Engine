"""
@file scene.py
@brief Renderes a scene of the game
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

from render.world.world import World
from utils.block_marker.block_marker import BlockMarker


class Scene:
    def __init__(self, app) -> None:
        """
        Initializes the scene.
        :param app: The main application
        """
        self.app = app
        self.world = World(self.app)
        self.block_marker = BlockMarker(self.world.block_handler)

    def update(self) -> None:
        """
        Updates the scene.
        """
        self.world.update()
        self.block_marker.update()

    def render(self) -> None:
        """
        Renders the scene.
        """
        self.world.render()
        self.block_marker.render()
