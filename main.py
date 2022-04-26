import pygame
from pygame.locals import (
    K_ESCAPE,
    K_s,
    K_x,
    KMOD_META,
    KEYDOWN,
    QUIT,
    MOUSEBUTTONDOWN,
    MOUSEMOTION,
    MOUSEBUTTONUP
)
import sys
import math
from itertools import cycle
from random import randint
from os import mkdir

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750


class ColorButton(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((150, 60))
        self.surf.fill("#FF6700")
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH / 2, 680))
        self.colors = cycle(("#FF6700", "#CCFF00"))
        self.color = next(self.colors)
        self.subcircle_rad = 0
        self.click_pos = None

    def update(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, "Black", self.rect.inflate(20, 20), 10, 10)
        if self.subcircle_rad:
            self.subcircle_rad += 15
            pygame.draw.circle(
                    self.surf,
                    self.color,
                    self.click_pos,
                    self.subcircle_rad)
        if self.subcircle_rad - 30 > self.rect.w:
            self.subcircle_rad = 0

    def activate(self, click_pos) -> str:
        color = next(self.colors)
        self.color = color
        self.subcircle_rad += 1
        # Refines clicking position to more accurately resemble the mouse
        click_pos = (
                click_pos[0] - self.rect.centerx + 80,
                click_pos[1] - self.rect.centery + 35
                )
        self.click_pos = click_pos
        return color


class Game:
    def __init__(self):
        try:
            # Creates a folder for saved images
            mkdir("creations")
        except FileExistsError:
            pass
        # -Setup-
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Highlighter 2")

        # -Game Stuff-
        self.drawing = False
        self.last_pos = None
        self.color = "#FF6700"
        self.color_btn = ColorButton()

    def set_screen(self):
        self.screen.fill("White")
        for i in range(1, 25):
            pygame.draw.line(
                    self.screen,
                    "Light Blue",
                    (0, i * 30),
                    (SCREEN_WIDTH, i * 30)
                    )
        pygame.draw.line(self.screen, "Red", (90, 0), (90, SCREEN_HEIGHT), 1)

    def run(self):
        self.set_screen()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    elif event.key == K_s:
                        mods = pygame.key.get_mods()
                        # Checks if cmd key is pressed
                        if mods & KMOD_META:
                            pygame.image.save(
                                    self.screen,
                                    f"creations/masterpiece-{randint(1, 10000)}.png")

                    elif event.key == K_x:
                        # Resets screen
                        self.set_screen()

                elif event.type == MOUSEMOTION:
                    if self.drawing:
                        mouse_position = pygame.mouse.get_pos()
                        if self.last_pos is not None:
                            pygame.draw.line(
                                    self.screen,
                                    self.color,
                                    self.last_pos,
                                    mouse_position,
                                    30)
                            pygame.draw.circle(
                                    self.screen,
                                    self.color,
                                    mouse_position,
                                    14
                                    )
                        self.last_pos = mouse_position

                elif event.type == MOUSEBUTTONUP:
                    mouse_position = (0, 0)
                    self.drawing = False

                elif event.type == MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()
                    self.drawing = True
                    if self.last_pos is not None:
                        dist = math.hypot(
                                mouse_position[0]-self.last_pos[0],
                                mouse_position[1]-self.last_pos[1]
                                )
                        if dist > 20:
                            self.last_pos = mouse_position
                    pygame.draw.circle(
                            self.screen,
                            self.color,
                            mouse_position,
                            14
                            )

                    if self.color_btn.rect.collidepoint(mouse_position) and not self.color_btn.subcircle_rad:
                        self.color = self.color_btn.activate(mouse_position)

            self.screen.blit(self.color_btn.surf, self.color_btn.rect)
            self.color_btn.update()

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
        pygame.display.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
