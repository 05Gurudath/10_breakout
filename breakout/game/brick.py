"""
Brick: a single destructible block.
"""
import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    def __init__(
        self,
        x,
        y,
        width,
        height,
        brick_type=NORMAL
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        # Set hit points based on brick type
        if brick_type == self.NORMAL:
            self.hits_remaining = 1
            self.color = (200, 90, 90)

        elif brick_type == self.STRONG:
            self.hits_remaining = 3
            self.color = (230, 180, 50)

        elif brick_type == self.UNBREAKABLE:
            self.hits_remaining = float("inf")
            self.color = (80, 80, 80)

        else:
            self.hits_remaining = 1
            self.color = (200, 90, 90)

    def get_rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )
