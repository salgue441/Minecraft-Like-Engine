"""
@file engine.py
@brief Contains the main engine class for the game. 
       This class is responsible for the main loop and the game window.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

from settings import WIN_RES
import moderngl as mg
import pygame as pg
import sys

"""
@brief Main engine class for the game.
"""


class Engine:
    def __init__(self) -> None:
        """
        Initializes the engine.
        """
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 6)
        pg.display.gl_set_attribute(
            pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE
        )

        pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)

        # Create the context
        self.ctx = mg.create_context()
        self.ctx.enable(flags=mg.DEPTH_TEST | mg.BLEND | mg.CULL_FACE)
        self.ctx.gc_mode = "auto"

        # Clock
        self.clock = pg.time.Clock()
        self.delta_time = 0.0

        self.is_running = True

    def update(self) -> None:
        """
        Updates the window and the clock
        """
        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")

    def render(self) -> None:
        """
        Renders content to the window
        """
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        pg.display.flip()

    def handle_events(self) -> None:
        """
        Handles all the game related events such as input
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.is_running = False
                pg.quit()
                sys.exit()

    def run(self) -> None:
        """
        Main loop of the game
        """
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()

        pg.quit()
        sys.exit()
