"""
@file scene.py
@brief Renderes a scene of the game
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

from render.world.world import World


class Scene:
    def __init__(self, app) -> None:
        """
        Initializes the scene.
        :param app: The main application
        """
        self.app = app
        self.world = World(self.app)

    def update(self) -> None:
        """
        Updates the scene.
        """
        self.world.update()

    def render(self) -> None:
        """
        Renders the scene.
        """
        self.world.render()
