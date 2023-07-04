"""
@file window.py
@brief Contains the main window class for the game.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""
from core.constants.settings import BG_COLOR, WIN_RES
import moderngl as mg
import pygame as pg
import sys


class Window:
    def __init__(self, resolution) -> None:
        """
        Initializes the window
        """
        self.resolution = resolution
        self.screen = None

    def create_window(self) -> None:
        """
        Creates the game window
        """
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 6)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )

        self.screen = pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)

    def clear_window(self) -> None:
        """
        Clears the window
        """
        self.screen.fill(color=BG_COLOR)
        pg.display.flip()

    def close_window(self) -> None:
        """
        Closes the window
        """
        pg.quit()
        sys.exit()
