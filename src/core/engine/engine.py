"""
@file engine.py
@brief Contains the main engine class for the game. 
       This class is responsible for the main loop and the game window.
@author Carlos Salguero
@version 1.0
@date 2023-07-04
"""

# Project files
from core.constants.settings import BG_COLOR, WIN_RES
from core.window.window import Window
from utils.shader_program.shader_program import ShaderProgram
from render.scene.scene import Scene
from player.player import Player
from graphics.texture.texture import Texture

# Libraries
import moderngl as mg
import pygame as pg

"""
@brief Main engine class for the game.
"""


class Engine:
    def __init__(self) -> None:
        """
        Initializes the engine.
        """
        self.window = Window(resolution=WIN_RES)

        # Clock
        self.clock = None
        self.delta_time = 0.0
        self.is_running = True

    def init_engine(self) -> None:
        """
        Initializes the engine
        """
        self.window.create_window()

        # Create the context
        self.ctx = mg.create_context()
        self.ctx.enable(flags=mg.DEPTH_TEST | mg.BLEND | mg.CULL_FACE)
        self.ctx.gc_mode = "auto"

        # Clock
        self.clock = pg.time.Clock()

        # Mouse overflow
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        # Textures
        self.texture = Texture(app=self)

        # Player
        self.player = Player(app=self)

        # Shaders and scene
        self.shader_program = ShaderProgram(app=self)
        self.scene = Scene(app=self)

    def update(self) -> None:
        """
        Updates the window and the clock
        """
        self.player.update()
        self.shader_program.update()
        self.scene.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption(f"FPS: {self.clock.get_fps():.2f}")

    def render(self) -> None:
        """
        Renders content to the window
        """
        self.ctx.clear(color=BG_COLOR)
        self.scene.render()
        self.window.clear_window()

    def handle_events(self) -> None:
        """
        Handles all the game related events such as input
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                self.is_running = False
                self.window.close_window()

    def run(self) -> None:
        """
        Main loop of the game
        """
        self.init_engine()

        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
